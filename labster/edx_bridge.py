from functools import partial

import requests

from django.conf import settings
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.files.uploadedfile import InMemoryUploadedFile

from cache_toolbox.core import del_cached_content
from contentstore.utils import add_instructor, initialize_permissions, course_image_url
from contentstore.views.item import _duplicate_item
from courseware.courses import get_course_by_id, get_course
from opaque_keys.edx.keys import UsageKey
from opaque_keys.edx.locations import SlashSeparatedCourseKey
from student.roles import CourseRole
from student.models import UserProfile
from xmodule.contentstore.content import StaticContent
from xmodule.contentstore.django import contentstore
from xmodule.modulestore.django import modulestore
from xmodule.modulestore.exceptions import InvalidLocationError


from labster.constants import COURSE_ID


def get_master_quiz_blocks():
    course_key = SlashSeparatedCourseKey.from_deprecated_string(COURSE_ID)
    course = get_course_by_id(course_key)

    quiz_blocks_by_lab = {}

    for section in course.get_children():
        for lab in section.get_children():  # sub section
            for quiz_blocks in lab.get_children():  # unit
                lab_name = lab.display_name.upper()
                if lab_name not in quiz_blocks_by_lab:
                    quiz_blocks_by_lab[lab_name] = {
                        'lab': lab,
                        'quiz_blocks': [quiz_blocks],
                    }
                else:
                    quiz_blocks_by_lab[lab_name]['quiz_blocks'].append(quiz_blocks)

    return quiz_blocks_by_lab


def get_lab_by_name(name):
    return get_master_quiz_blocks().get(name.upper())


def duplicate_lab_content(user, source_location, parent_location):
    store = modulestore()
    parent_locator = UsageKey.from_string(parent_location)
    source_locator = UsageKey.from_string(source_location)
    source_item = store.get_item(source_locator)
    parent_item = store.get_item(parent_locator)

    # delete parent's children first
    for child in parent_item.get_children():
        store.delete_item(child.location, user.id)

    # duplicate quiz_blocks
    for quiz_block in source_item.get_children():
        new_location = _duplicate_item(parent_locator, quiz_block.location, user=user, display_name=quiz_block.display_name)
        modulestore().publish(new_location, user.id)


def get_or_create_course(source, target, user):
    source_course = get_course_by_id(SlashSeparatedCourseKey.from_deprecated_string(source))

    display_name = source_course.display_name
    org, number, run = target.split('/')

    course_key = SlashSeparatedCourseKey(org, number, run)
    fields = {'display_name': display_name}

    wiki_slug = u"{0}.{1}.{2}".format(course_key.org, course_key.course, course_key.run)
    definition_data = {'wiki_slug': wiki_slug}
    fields.update(definition_data)

    try:
        if CourseRole.course_group_already_exists(course_key):
            raise InvalidLocationError()

        course = modulestore().create_course(
            course_key.org,
            course_key.course,
            course_key.run,
            user.id,
            fields=fields,
        )

    except InvalidLocationError:
        course = get_course(course_key)

    else:
        # Make sure user has instructor and staff access to the new course
        add_instructor(course.id, user, user)

        # Initialize permissions for user in the new course
        initialize_permissions(course.id, user)

    return course


def force_create_course(source, target, user, extra_fields=None):
    source_course = get_course_by_id(SlashSeparatedCourseKey.from_deprecated_string(source))
    display_name = source_course.display_name
    fields = {'display_name': display_name}

    course = None
    start_index = 0
    org, original_number, run = target.split('/')

    number = original_number
    while course is None:
        course_key = SlashSeparatedCourseKey(org, number, run)

        wiki_slug = u"{0}.{1}.{2}".format(course_key.org, course_key.course, course_key.run)
        definition_data = {'wiki_slug': wiki_slug}
        fields.update(definition_data)
        if extra_fields:
            fields.update(extra_fields)

        try:
            if CourseRole.course_group_already_exists(course_key):
                raise InvalidLocationError()

            course = modulestore().create_course(
                course_key.org,
                course_key.course,
                course_key.run,
                user.id,
                fields=fields,
            )

        except InvalidLocationError:
            start_index += 1
            number = "{}{}".format(original_number, start_index)
            continue

        else:
            # Make sure user has instructor and staff access to the new course
            add_instructor(course.id, user, user)

            # Initialize permissions for user in the new course
            initialize_permissions(course.id, user)

    UserProfile.objects\
        .filter(user_id=user.id)\
        .exclude(user_type=UserProfile.USER_TYPE_TEACHER)\
        .update(user_type=UserProfile.USER_TYPE_TEACHER)

    return course


def duplicate_course(source, target, user, extra_fields=None, http_protocol='https'):
    source_course = get_course_by_id(SlashSeparatedCourseKey.from_deprecated_string(source))
    target_course = force_create_course(source, target, user, extra_fields)

    new_course_key = str(target_course.location.course_key)
    image_url = "{}://{}{}".format(http_protocol, settings.LMS_BASE, course_image_url(source_course))
    upload_image_from_url(new_course_key, image_url)

    for child in target_course.get_children():
        modulestore().delete_item(child.location, user.id)

    target_locator = target_course.location

    for child in source_course.get_children():
        new_location = _duplicate_item(target_locator, child.location, user=user, display_name=child.display_name)
        modulestore().publish(new_location, user.id)

    return target_course


def upload_image_from_url(course, url):
    res = requests.get(url)

    assert res.status_code == 200, "invalid status code {}".format(res.status_code)

    name = url.split('/')[-1]
    content = res.content
    content_type = res.headers.get('content-type')
    size = len(content)
    charset = res.headers.get('encoding')

    temp_file = NamedTemporaryFile(delete=True)
    temp_file.write(content)
    temp_file.flush()

    upload_file = InMemoryUploadedFile(
        File(temp_file), 'file',
        name, content_type, size, charset)

    course_key = SlashSeparatedCourseKey.from_deprecated_string(course)
    upload_image(course_key, upload_file)


def upload_image(course_key, upload_file):
    filename = upload_file.name
    mime_type = upload_file.content_type

    content_loc = StaticContent.compute_location(course_key, filename)

    chunked = upload_file.multiple_chunks()
    sc_partial = partial(StaticContent, content_loc, filename, mime_type)
    if chunked:
        content = sc_partial(upload_file.chunks())
        tempfile_path = upload_file.temporary_file_path()
    else:
        content = sc_partial(upload_file.read())
        tempfile_path = None

    # first let's see if a thumbnail can be created
    (thumbnail_content, thumbnail_location) = contentstore().generate_thumbnail(
        content,
        tempfile_path=tempfile_path
    )

    # delete cached thumbnail even if one couldn't be created this time (else
    # the old thumbnail will continue to show)
    del_cached_content(thumbnail_location)
    # now store thumbnail location only if we could create it
    if thumbnail_content is not None:
        content.thumbnail_location = thumbnail_location

    # then commit the content
    contentstore().save(content)
    del_cached_content(content.location)

    # readback the saved content - we need the database timestamp
    # readback = contentstore().find(content.location)

    # locked = getattr(content, 'locked', False)
    # response_payload = {
    #     'asset': _get_asset_json(content.name, readback.last_modified_at, content.location, content.thumbnail_location, locked),
    #     'msg': _('Upload completed')
    # }

    # return JsonResponse(response_payload)

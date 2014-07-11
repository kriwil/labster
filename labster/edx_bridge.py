from contentstore.utils import get_modulestore
from contentstore.views.helpers import _xmodule_recurse
from contentstore.views.item import _duplicate_item
from courseware.courses import get_course_by_id
from opaque_keys.edx.keys import UsageKey
from opaque_keys.edx.locations import SlashSeparatedCourseKey


def get_master_quiz_blocks():
    course_id = "LabsterX/LAB101/2014_LAB"
    course_key = SlashSeparatedCourseKey.from_deprecated_string(course_id)
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
    parent_locator = UsageKey.from_string(parent_location)
    source_locator = UsageKey.from_string(source_location)
    source_store = get_modulestore(source_locator)
    source_item = source_store.get_item(source_locator)

    # delete parent's children first
    parent_store = get_modulestore(parent_locator)
    parent_item = parent_store.get_item(parent_locator)

    for child in parent_item.get_children():
        store = get_modulestore(child.location)
        item = store.get_item(child.location)
        _xmodule_recurse(item, lambda i: store.delete_item(i.location, delete_all_versions=True))

    def _publish(block):
        # This is super gross, but prevents us from publishing something that
        # we shouldn't. Ideally, all modulestores would have a consistant
        # interface for publishing. However, as of now, only the DraftMongoModulestore
        # does, so we have to check for the attribute explicitly.
        store = get_modulestore(block.location)
        store.publish(block.location, user.id)

    for quiz_block in source_item.get_children():
        duplicated = _duplicate_item(parent_locator, quiz_block.location, quiz_block.display_name, user)
        item = source_store.get_item(duplicated)
        _xmodule_recurse(
            item,
            _publish
        )

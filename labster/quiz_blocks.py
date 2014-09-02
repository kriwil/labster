import json

from lxml import etree
import requests

from contentstore.views.item import _create_item, _save_xblock
from opaque_keys.edx.keys import UsageKey
from xmodule.modulestore.django import modulestore

from labster.models import Lab
from labster.utils import get_request

QUIZ_BLOCK_S3_PATH = "https://s3-us-west-2.amazonaws.com/labster/uploads/{}"


def create_xblock(user, category, parent_location, name=None, extra_post=None):
    post_data = {
        'parent_locator': parent_location,
        'category': category,
    }

    if name:
        post_data['display_name'] = name

    if extra_post:
        post_data.update(extra_post)

    request = get_request(user, json.dumps(post_data))
    response = _create_item(request)
    response_content = json.loads(response.content)
    section_location = response_content['locator']
    usage_key = UsageKey.from_string(section_location)
    store = modulestore()

    return store.get_item(usage_key)


def update_problem(user, xblock, data, name, platform_xml):
    nullout = ["markdown"]
    metadata = {
        'display_name': name,
        'platform_xml': platform_xml,
    }

    return _save_xblock(
        user,
        xblock,
        data=data,
        nullout=nullout,
        metadata=metadata,
    )


def update_quizblocks(course, user, section_name='Labs', command=None):

    section_dicts = {section.display_name: section for section in course.get_children()}
    course_location = course.location.to_deprecated_string()

    # required_section_names = ['Labs']
    if section_name not in section_dicts:
        command and command.stdout.write("creating {}\n".format(section_name))
        section_dicts[section_name] = create_xblock(user, 'chapter', course_location, name=section_name)

    section = section_dicts[section_name]
    section_location = section.location.to_deprecated_string()
    sub_section_dicts = {sub.display_name: sub for sub in section.get_children()}

    labs = Lab.objects.all()
    for lab in labs:
        if lab.name not in sub_section_dicts:
            command and command.stdout.write("creating {}\n".format(lab.name))
            sub_section_dicts[lab.name] = create_xblock(user, 'sequential', section_location, name=lab.name)

        quizblock_xml = lab.engine_xml.replace('Engine_', 'QuizBlocks_')
        quizblock_xml = QUIZ_BLOCK_S3_PATH.format(quizblock_xml)

        response = requests.get(quizblock_xml)
        if response.status_code != 200:
            return

        tree = etree.fromstring(response.content)
        sub_section = sub_section_dicts[lab.name]
        sub_section_location = sub_section.location.to_deprecated_string()

        unit_dicts = {qb.display_name: qb for qb in sub_section.get_children()}

        for quizblock in tree.getchildren():
            name = quizblock.attrib.get('Id')
            if name not in unit_dicts:
                command and command.stdout.write("creating quizblock {}\n".format(name))
                unit_dicts[name] = create_xblock(user, 'vertical', sub_section_location, name=name)

            unit = unit_dicts[name]
            unit_location = unit.location.to_deprecated_string()
            problem_dicts = {problem.display_name: problem for problem in unit.get_children()}

            for quiz in quizblock.getchildren():
                name = quiz.attrib.get('Id')

                if name not in problem_dicts:
                    command and command.stdout.write("creating problem {}\n".format(name))
                    extra_post = {'boilerplate': "multiplechoice.yaml"}
                    problem_dicts[name] = create_xblock(user, 'problem', unit_location, extra_post=extra_post)

                problem_xblock = problem_dicts[name]
                data = etree.tostring(quiz, pretty_print=True)
                update_problem(user, problem_xblock, data, name=name, platform_xml=data)

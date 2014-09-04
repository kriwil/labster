import hashlib
import json

from lxml import etree
import requests

from opaque_keys.edx.keys import UsageKey
from xmodule.modulestore.django import modulestore

from labster.models import Lab, ProblemProxy
from labster.parsers.problem_parsers import QuizParser, ProblemParser
from labster.utils import get_request

QUIZ_BLOCK_S3_PATH = "https://s3-us-west-2.amazonaws.com/labster/uploads/{}"


def create_xblock(user, category, parent_location, name=None, extra_post=None):
    from contentstore.views.item import _create_item

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


def update_problem(user, xblock, data, name, platform_xml, correct_index=None,
                   correct_answer=''):
    from contentstore.views.item import _save_xblock

    nullout = ["markdown"]
    metadata = {
        'display_name': name,
        'platform_xml': platform_xml,
        'correct_index': correct_index,
        'correct_answer': correct_answer,
    }

    response = _save_xblock(
        user,
        xblock,
        data=data,
        nullout=nullout,
        metadata=metadata,
        publish='make_public',
    )

    new_xblock = json.loads(response.content)
    locator = UsageKey.from_string(new_xblock['id'])
    modulestore().publish(locator, user.id)
    return new_xblock


def update_quizblocks(course, user, section_name='Labs', command=None, is_master=False):

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
                platform_xml = etree.tostring(quiz, pretty_print=True)

                quiz_parser = QuizParser(quiz)
                if is_master:
                    edx_xml = platform_xml
                else:
                    edx_xml = quiz_parser.parsed_as_string

                update_problem(user, problem_xblock, data=edx_xml, name=name,
                               platform_xml=platform_xml,
                               correct_index=quiz_parser.correct_index,
                               correct_answer=quiz_parser.correct_answer)


def sync_quiz_xml(course, user, section_name='Labs', sub_section_name='', command=None):

    section_dicts = {section.display_name: section for section in course.get_children()}

    section = section_dicts[section_name]
    sub_section_dicts = {sub.display_name: sub for sub in section.get_children()}

    if sub_section_name:
        labs = [sub_section_name]
    else:
        labs = Lab.objects.all()
        labs = [lab.name for lab in labs]

    for lab_name in labs:
        sub_section = sub_section_dicts[lab_name]

        for qb in sub_section.get_children():
            for unit in qb.get_children():

                if not unit.platform_xml:
                    command and command.stdout.write("empty: {}\n".format(unit.display_name))
                    parser = ProblemParser(etree.fromstring(unit.data))
                    unit.platform_xml = parser.parsed_as_string
                    unit.correct_answer = parser.correct_answer
                    unit.correct_index = parser.correct_index

                elif unit.data == unit.platform_xml:
                    command and command.stdout.write("converting to data: {}\n".format(unit.display_name))
                    parser = QuizParser(etree.fromstring(unit.platform_xml))
                    unit.data = parser.parsed_as_string

                modulestore().update_item(unit, user.id)
                modulestore().publish(unit.location, user.id)

            modulestore().publish(qb.location, user.id)
        modulestore().publish(sub_section.location, user.id)


def get_location_by_problem(lab_proxy, question):
    hashed = hashlib.md5(question.encode('utf-8').strip()).hexdigest()

    try:
        obj = ProblemProxy.objects.get(lab_proxy=lab_proxy, question=hashed)
    except ProblemProxy.DoesNotExist:
        pass
    else:
        return obj.location

    location = ''
    locator = UsageKey.from_string(lab_proxy.location)
    descriptor = modulestore().get_item(locator)

    for _quiz_block in descriptor.get_children():
        for _problem in _quiz_block.get_children():
            tree = etree.fromstring(_problem.platform_xml)
            _question = tree.attrib.get('Sentence')
            _hashed = hashlib.md5(_question.encode('utf-8').strip()).hexdigest()
            _location = str(_problem.location)

            if hashed == _hashed:
                location = _location

            ProblemProxy.objects.get_or_create(
                lab_proxy=lab_proxy, question=_hashed,
                defaults={'location': _location},
            )

    return location

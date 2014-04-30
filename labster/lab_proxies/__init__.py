from collections import OrderedDict

from courseware.courses import get_course
from courseware.model_data import FieldDataCache
from xmodule.modulestore.django import modulestore


class LabProxyData(object):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.get('request')
        self.user = kwargs.get('user')
        self.lab_proxy = kwargs.get('lab_proxy')

        self.problemset = OrderedDict()
        self.problem_by_id = {}

        course_id = self.lab_proxy.course_id
        chapter = self.lab_proxy.chapter_id
        section = self.lab_proxy.section_id
        course = get_course(course_id=course_id)

        chapter_descriptor = course.get_child_by(lambda m: m.url_name == chapter)

        section_descriptor = chapter_descriptor.get_child_by(lambda m: m.url_name == section)
        section_descriptor = modulestore().get_instance(course.id, section_descriptor.location, depth=None)

        section_field_data_cache = FieldDataCache.cache_for_descriptor_descendents(
            course.id, self.user, section_descriptor, depth=2)

        self.section_field_data_cache = section_field_data_cache
        self.course = course

    def get_problemset(self):
        """
        A better structured problemset
        quiz_block_id = {
            id: quizblock_id,
            module: quizblock_module,
            problems: [list, of, problem],
        }
        """

        if not self.problemset:
            problemset = OrderedDict()
            quizblock = None

            # descriptors store all the xmodule/xblock
            for each in self.section_field_data_cache.descriptors:
                if each.plugin_name == 'quizblock':
                    if quizblock and len(quizblock['problems']):
                        problemset[quizblock['id']] = quizblock
                        quizblock = None

                    quizblock = {
                        'id': each.quizblock_id,
                        'description': each.description,
                        'module': each,
                        'problems': [],
                    }

                if each.plugin_name == 'problem' and each.data:
                    quizblock['problems'].append(each)
                    self.problem_by_id[each.location.name] = each

            if quizblock and len(quizblock['problems']):
                problemset[quizblock['id']] = quizblock
                quizblock = None

            self.problemset = problemset
        return self.problemset

    def get_problem_by_id(self, problem_id):
        self.get_problemset()
        return self.problem_by_id.get(problem_id)

import re

from html2text import HTML2Text
from lxml import etree


class MultipleChoiceProblemParser(object):

    def __init__(self, xml):
        self.xml = xml
        comp = re.compile(
            r'<problem>(.+)<multiplechoiceresponse>(.+)</multiplechoiceresponse>.+<solution>(.+)</solution>',
            re.DOTALL | re.IGNORECASE)

        found = comp.search(self.xml)
        self.raw_problem, self.raw_options, self.raw_solution = found.groups()

    def _parse_problem(self):
        parser = HTML2Text(baseurl='')
        parser.body_width = 0
        problem = parser.handle(self.raw_problem)
        return problem.strip()

    def _parse_options(self):
        tree = etree.fromstring(self.raw_options)
        choices = []
        for each in tree.iter():
            if each.tag != 'choice':
                continue

            choice = {
                'text': each.text.strip(),
                'is_correct': each.attrib.get('correct') == 'true',
            }
            choices.append(choice)
        return choices

    def _parse_solution(self):
        text = ""
        tree = etree.fromstring(self.raw_solution)
        for each in tree.iter():
            if each.tag != 'p':
                continue

            if each.text.strip().lower() == 'explanation':
                continue

            text = each.text.strip()
        return text

    @property
    def problem(self):
        return self._parse_problem()

    @property
    def options(self):
        return self._parse_options()

    @property
    def solution(self):
        return self._parse_solution()


class QuizParser(object):

    def __init__(self, quiz_tree):
        self.quiz_tree = quiz_tree
        self._parsed = None
        self._parsed_as_string = ""

    @property
    def parsed(self):
        if self._parsed:
            return self._parsed

        correct_message = self.quiz_tree.attrib.get('CorrectMessage', '')
        sentence = self.quiz_tree.attrib.get('Sentence', '')
        # wrong_message = self.quiz_tree.attrib.get('WrongMessage', '')

        problem_el = etree.Element('problem')
        p_el = etree.SubElement(problem_el, 'p')
        p_el.text = sentence

        multiplechoice_el = etree.SubElement(problem_el, 'multiplechoiceresponse')
        choicegroup_el = etree.SubElement(multiplechoice_el, 'choicegroup',
                                       {'type': "MultipleChoice",
                                        'label': sentence,
                                        })

        for options in self.quiz_tree.getchildren():
            for option in options.getchildren():
                correct = 'true' if option.attrib.get('IsCorrectAnswer') == 'true' else 'false'
                choice_el = etree.SubElement(choicegroup_el, 'choice', {'correct': correct})
                choice_el.text = option.attrib.get('Sentence')

        solution_el = etree.SubElement(problem_el, 'solution')
        div_el = etree.SubElement(solution_el, 'div', {'class': "detailed-solution"})
        p_el = etree.SubElement(div_el, 'p')
        p_el.text = 'Explanation'
        p_el = etree.SubElement(div_el, 'p')
        p_el.text = correct_message

        self._parsed = problem_el
        print etree.tostring(problem_el, pretty_print=True)
        return self._parsed

    @property
    def parsed_as_string(self):
        if self._parsed_as_string:
            return self._parsed_as_string

        self._parsed_as_string = etree.tostring(self.parsed, pretty_print=True)
        return self._parsed_as_string

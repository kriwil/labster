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


class ProblemParser(object):

    def __init__(self, problem_tree, id=''):
        self.problem_tree = problem_tree
        self.id = id
        self._parsed = None
        self._parsed_as_string = ""
        self._correct_index = None
        self._correct_answer = ''

    @property
    def parsed(self):
        if self._parsed:
            return self._parsed

        quiz_attrib = {
            'Id': self.id,
            'CorrectMessage': "",
            'WrongMessage': "No. This is incorrect - please try again!",
            'Sentence': "",
        }
        sentences = []
        correct_messages = []
        for each in self.problem_tree.getchildren():
            if each.tag != 'p':
                break
            sentences.append(each.text.strip())

        for each in self.problem_tree.getchildren():
            if each.tag == 'solution':
                for div in each.getchildren():
                    for p in div.getchildren():
                        if p.text.upper() != 'EXPLANATION':
                            correct_messages.append(p.text.strip())

        quiz_attrib['Sentence'] = '\n'.join(sentences)
        quiz_attrib['CorrectMessage'] = '\n'.join(correct_messages)
        quiz_el = etree.Element('Quiz', quiz_attrib)

        for each in self.problem_tree.getchildren():
            if each.tag == 'multiplechoiceresponse':
                for choicegroup in each.getchildren():
                    options = etree.SubElement(quiz_el, 'Options')

                    for index, option in enumerate(choicegroup.getchildren(), index=0):
                        attrib = {'Sentence': option.text}

                        if option.attrib.get('correct') == 'true':
                            attrib['IsCorrectAnswer'] = 'true'
                            self._correct_answer = option.text
                            self._correct_index = index

                        etree.SubElement(options, 'Option', **attrib)

        self._parsed = quiz_el

        return quiz_el

    @property
    def parsed_as_string(self):
        if self._parsed_as_string:
            return self._parsed_as_string

        self._parsed_as_string = etree.tostring(self.parsed, pretty_print=True)
        return self._parsed_as_string

    @property
    def correct_index(self):
        if self._correct_index:
            return self._correct_index

        return self._correct_index

    @property
    def correct_answer(self):
        if self._correct_answer:
            return self._correct_answer

        return self._correct_answer


class QuizParser(object):

    def __init__(self, quiz_tree):
        self.quiz_tree = quiz_tree
        self._parsed = None
        self._parsed_as_string = ""
        self._correct_index = None
        self._correct_answer = ''

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
            for index, option in enumerate(options.getchildren(), start=0):
                sentence = option.attrib.get('Sentence')
                correct = 'false'
                if option.attrib.get('IsCorrectAnswer'):
                    correct = 'true'
                    self._correct_index = index
                    self._correct_answer = sentence

                choice_el = etree.SubElement(choicegroup_el, 'choice', {'correct': correct})
                choice_el.text = sentence

        solution_el = etree.SubElement(problem_el, 'solution')
        div_el = etree.SubElement(solution_el, 'div', {'class': "detailed-solution"})
        p_el = etree.SubElement(div_el, 'p')
        p_el.text = 'Explanation'
        p_el = etree.SubElement(div_el, 'p')
        p_el.text = correct_message

        self._parsed = problem_el
        return self._parsed

    @property
    def parsed_as_string(self):
        if self._parsed_as_string:
            return self._parsed_as_string

        self._parsed_as_string = etree.tostring(self.parsed, pretty_print=True)
        return self._parsed_as_string

    @property
    def correct_index(self):
        if self._correct_index:
            return self._correct_index

        return self._correct_index

    @property
    def correct_answer(self):
        if self._correct_answer:
            return self._correct_answer

        return self._correct_answer

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

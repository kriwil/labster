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

    xml_template = """
<problem>
<p>A multiple choice problem presents radio buttons for student input. Students can only select a single option presented. Multiple Choice questions have been the subject of many areas of research due to the early invention and adoption of bubble sheets.</p>

<p>One of the main elements that goes into a good multiple choice question is the existence of good distractors. That is, each of the alternate responses presented to the student should be the result of a plausible mistake that a student might make.</p>

<p>What Apple device competed with the portable CD player?</p>
<multiplechoiceresponse>
  <choicegroup label="What Apple device competed with the portable CD player?" type="MultipleChoice">
    <choice correct="false">The iPad</choice>
    <choice correct="false">Napster</choice>
    <choice correct="true">The iPod</choice>
    <choice correct="false">The vegetable peeler</choice>
  </choicegroup>
</multiplechoiceresponse>


<solution>
<div class="detailed-solution">
<p>Explanation</p>

<p>The release of the iPod allowed consumers to carry their entire music library with them in a format that did not rely on fragile and energy-intensive spinning disks.</p>

</div>
</solution>

</problem>
    """

    def __init__(self, quiz_tree):
        self.quiz_tree = quiz_tree
        self._parsed = ""

    @property
    def parsed(self):
        if self._parsed:
            return self._parsed

        problem = etree.Element('problem')
        p_el = etreeSubElement(problem, 'p')

        correct_message = self.quiz_tree.attrib.get('CorrectMessage', '')
        sentence = self.quiz_tree.attrib.get('sentence', '')
        wrong_message = self.quiz_tree.attrib.get('WrongMessage', '')

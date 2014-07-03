import unittest

from labster.utils import xml_to_markdown, answer_from_xml, markdown_to_xml, xml_to_html


multiple_xml_string = """
<problem>
<p>What Apple device competed with the portable CD player?</p>
<p>What Apple device competed with the portable CD player?</p>
<multiplechoiceresponse>
<choicegroup type="MultipleChoice">
<choice correct="false">The iPad</choice>
<choice correct="false">Napster</choice>
<choice correct="true">The iPod</choice>
<choice correct="false">The vegetable peeler</choice>
</choicegroup>
</multiplechoiceresponse>
<solution>
<div class="detailed-solution">
<p>Explanation</p>
<p>The release of the iPod allowed consumers to carry their entire music library with them in a
format that did not rely on fragile and energy-intensive spinning disks.</p>
</div>
</solution>
</problem>
"""

multiple_markdown_string = """
What Apple device competed with the portable CD player?

What Apple device competed with the portable CD player?

( ) The iPad
( ) Napster
(x) The iPod
( ) The vegetable peeler

[explanation]
The release of the iPod allowed consumers to carry their entire music library with them in a
format that did not rely on fragile and energy-intensive spinning disks.
[explanation]
"""

multiple_html_string = """
<problem>
<p>What Apple device competed with the portable CD player?</p>
<p>What Apple device competed with the portable CD player?</p>
<multiplechoiceresponse>
<choicegroup type="MultipleChoice">
<label><input name="radio-input" type="radio" value="The iPad" correct="false"> The iPad</label>
<label><input name="radio-input" type="radio" value="Napster" correct="false"> Napster</label>
<label><input name="radio-input" type="radio" value="The iPod" correct="true"> The iPod</label>
<label><input name="radio-input" type="radio" value="The vegetable peeler" correct="false"> The vegetable peeler</label>
</choicegroup>
</multiplechoiceresponse>
<solution>
<div class="detailed-solution">
<p>Explanation</p>
<p>The release of the iPod allowed consumers to carry their entire music library with them in a
format that did not rely on fragile and energy-intensive spinning disks.</p>
</div>
</solution>
</problem>
"""

text_xml_string = """
<problem>
<p>Which US state has Lansing as its capital?</p>
<p>Which US state has Lansing as its capital?</p>
<stringresponse answer="Michigan" type="ci">
<textline size="20"/>
</stringresponse>
<solution>
<div class="detailed-solution">
<p>Explanation</p>
<p>Lansing is the capital of Michigan, although it is not Michgan's largest city,
or even the seat of the county in which it resides.</p>
</div>
</solution>
</problem>
"""

text_markdown_string = """
Which US state has Lansing as its capital?

Which US state has Lansing as its capital?

= Michigan

[explanation]
Lansing is the capital of Michigan, although it is not Michgan's largest city,
or even the seat of the county in which it resides.
[explanation]
"""

text_html_string = """
<problem>
<p>Which US state has Lansing as its capital?</p>
<p>Which US state has Lansing as its capital?</p>
<div><input name="text-input" type="text" value="Michigan"/></div>
<solution>
<div class="detailed-solution">
<p>Explanation</p>
<p>Lansing is the capital of Michigan, although it is not Michgan's largest city,
or even the seat of the county in which it resides.</p>
</div>
</solution>
</problem>
"""


class XmlToMarkdownTest(unittest.TestCase):

    def test_multiplechoice(self):
        markdown_string = xml_to_markdown(multiple_xml_string.strip())
        assert markdown_string.strip() == multiple_markdown_string.strip()

    def test_textinput(self):
        markdown_string = xml_to_markdown(text_xml_string.strip())
        assert markdown_string.strip() == text_markdown_string.strip()


class MarkdownToXmlTest(unittest.TestCase):

    def test_multiple_choice_xml(self):
        string = markdown_to_xml(multiple_markdown_string)
        assert string.strip() == multiple_xml_string.strip(), string

    def test_text_input_xml(self):
        string = markdown_to_xml(text_markdown_string)
        assert string.strip() == text_xml_string.strip(), string


class AnswerFromXmlTest(unittest.TestCase):

    def test_multiple_choice(self):
        real_answer = "the ipod"
        answer = answer_from_xml(multiple_xml_string)
        assert answer.lower() == real_answer.lower()

    def test_text_input(self):
        real_answer = "michigan"
        answer = answer_from_xml(text_xml_string)
        assert answer.lower() == real_answer.lower()


class XmlToHtmlTest(unittest.TestCase):

    def test_multiple_choice_html(self):
        string = xml_to_html(multiple_xml_string)
        assert string.strip() == multiple_html_string.strip(), string

    def test_text_choice_html(self):
        string = xml_to_html(text_xml_string)
        assert string.strip() == text_html_string.strip(), string


class MultipleConvertTest(unittest.TestCase):

    def test_text_input(self):
        string = markdown_to_xml(text_markdown_string)
        string = xml_to_markdown(string)

        assert string.strip() == text_markdown_string.strip(), string

    def test_multiple_input(self):
        string = markdown_to_xml(multiple_markdown_string)
        string = xml_to_markdown(string)

        assert string.strip() == multiple_markdown_string.strip(), string

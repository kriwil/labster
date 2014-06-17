from labster.utils import markdown_to_xml, xml_to_markdown


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


def test_multiple_choice_markdown():
    string = xml_to_markdown(multiple_xml_string)
    assert string.strip() == multiple_markdown_string.strip(), string


def test_text_input_markdown():
    string = xml_to_markdown(text_xml_string)
    assert string.strip() == text_markdown_string.strip(), string


def test_multiple_choice_xml():
    string = markdown_to_xml(multiple_markdown_string)
    assert string.strip() == multiple_xml_string.strip(), string


def test_text_input_xml():
    string = markdown_to_xml(text_markdown_string)
    assert string.strip() == text_xml_string.strip(), string


def test_text_input():
    string = markdown_to_xml(text_markdown_string)
    string = xml_to_markdown(string)

    assert string.strip() == text_markdown_string.strip(), string


def test_multiple_input():
    string = markdown_to_xml(multiple_markdown_string)
    string = xml_to_markdown(string)

    assert string.strip() == multiple_markdown_string.strip(), string


if __name__ == "__main__":
    test_multiple_choice_markdown()
    test_text_input_markdown()
    test_multiple_choice_xml()
    test_text_input_xml()
    test_multiple_input()
    test_text_input()

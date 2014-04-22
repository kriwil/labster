from labster.utils import xml_to_markdown

md_0 = """
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

xml_0 = """
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
<p>The release of the iPod allowed consumers to carry their entire music library with them in a </p>
<p>format that did not rely on fragile and energy-intensive spinning disks.</p>
</div>
</solution>
</problem>
"""

md_1 = """
Select the answer that matches

[ ] The iPad
[ ] Napster
[x] The iPod
[x] The vegetable peeler

[explanation]
The release of the iPod allowed consumers to carry their entire music library with them in a format that did not rely on fragile and energy-intensive spinning disks.
[explanation]
"""

xml_1 = """
<problem>
<p>Select the answer that matches</p>
<choiceresponse>
<checkboxgroup direction="vertical">
<choice correct="false">The iPad</choice>
<choice correct="false">Napster</choice>
<choice correct="true">The iPod</choice>
<choice correct="true">The vegetable peeler</choice>
</checkboxgroup>
</choiceresponse>
<solution>
<div class="detailed-solution">
<p>Explanation</p>
<p>The release of the iPod allowed consumers to carry their entire music library with them in a format that did not rely on fragile and energy-intensive spinning disks.</p>
</div>
</solution>
</problem>
"""

md_2 = """
Which US state has Lansing as its capital?

Which US state has Lansing as its capital?

= Michigan

[explanation]
Lansing is the capital of Michigan, although it is not Michgan's largest city,
or even the seat of the county in which it resides.
[explanation]
"""

xml_2 = """
<problem>
<p>Which US state has Lansing as its capital?</p>
<p>Which US state has Lansing as its capital?</p>
<stringresponse answer="Michigan" type="ci" >
<textline size="20"/>
</stringresponse>
<solution>
<div class="detailed-solution">
<p>Explanation</p>
<p>Lansing is the capital of Michigan, although it is not Michgan's largest city, </p>
<p>or even the seat of the county in which it resides.</p>
</div>
</solution>
</problem>
"""


class TestXmlToMarkdown:
    def test_multiplechoice(self):
        markdown_string = xml_to_markdown(xml_0.strip())
        assert markdown_string.strip() == md_0.strip()

    def test_checkbox(self):
        markdown_string = xml_to_markdown(xml_1.strip())
        assert markdown_string.strip() == md_1.strip()

    def test_textinput(self):
        markdown_string = xml_to_markdown(xml_2.strip())
        assert markdown_string.strip() == md_2.strip()

from lxml import etree

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


def choicegroup_xml_to_markdown(element_list, element_type='radio'):
    """
    Convert list of elements (xml) to list of element in markdown format
    """

    if element_type == 'radio':
        left_sep, right_sep = '(', ')'
    elif element_type == 'checkbox':
        left_sep, right_sep = '[', ']'
    else:
        raise Exception("Invalid element type.")

    output = []
    for choice in element_list:
        choice_str = "{left}{value}{right} {text}".format(
            left=left_sep,
            value="x" if choice.attrib['correct'] == 'true' else " ",
            right=right_sep,
            text=choice.text,
        )

        output.append(choice_str.strip())
    return output


def xml_to_markdown(xml_string):
    markdown_string = []
    string = xml_string
    string = string.replace("\n", "")

    root = etree.fromstring(string)
    for el in root:
        if el.tag == 'p':
            markdown_string.append(el.text.strip())
            markdown_string.append("")

        elif el.tag == 'multiplechoiceresponse':
            choicegroup = el.getchildren()[0]
            assert choicegroup.tag == 'choicegroup'
            assert choicegroup.attrib['type'].lower() == 'multiplechoice'

            choice_list = choicegroup_xml_to_markdown(choicegroup, 'radio')
            markdown_string.extend(choice_list)
            markdown_string.append("")

        elif el.tag == 'choiceresponse':
            checkboxgroup = el.getchildren()[0]
            assert checkboxgroup.tag == 'checkboxgroup'

            choice_list = choicegroup_xml_to_markdown(checkboxgroup, 'checkbox')
            markdown_string.extend(choice_list)
            markdown_string.append("")

        elif el.tag == 'stringresponse':
            answer = el.attrib.get('answer', "")
            answer_string = "= {}".format(answer)
            markdown_string.append(answer_string)
            markdown_string.append("")

        elif el.tag == 'solution':
            div = el.getchildren()[0]
            assert div.tag == 'div'
            assert div.attrib['class'] == 'detailed-solution'

            markdown_string.append("[explanation]")

            ps = div.getchildren()

            # first p is header
            for each in ps[1:]:
                markdown_string.append(each.text.strip())

            markdown_string.append("[explanation]")

    return "\n".join(markdown_string).strip()


if __name__ == "__main__":
    markdown_string = xml_to_markdown(xml_0.strip())
    assert markdown_string.strip() == md_0.strip()

    markdown_string = xml_to_markdown(xml_1.strip())
    assert markdown_string.strip() == md_1.strip()

    markdown_string = xml_to_markdown(xml_2.strip())
    assert markdown_string.strip() == md_2.strip()

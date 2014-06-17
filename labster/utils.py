import re

from lxml import etree
import markdown


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
    if not xml_string:
        return ""

    markdown_string = []
    string = xml_string

    parser = etree.XMLParser(remove_blank_text=True)
    root = etree.XML(string, parser=parser)
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


def markdown_to_xml(markdown_string):
    if not markdown_string:
        return ""

    xml_string = ""
    html_string = markdown.markdown(markdown_string)

    # choice
    html_string = html_string.replace("<p>(", """<multiplechoiceresponse>\n<choicegroup type="MultipleChoice">\n(""")
    html_string = re.sub(r'^(\(.+)<\/p>$', "\\1\n</choicegroup>\n</multiplechoiceresponse>", html_string, flags=re.M)
    html_string = re.sub(r'^\((.+)\)\s?(.+)$', """<choice correct="\\1">\\2</choice>""", html_string, flags=re.M)
    html_string = html_string.replace('correct=" "', 'correct="false"')
    html_string = html_string.replace('correct="x"', 'correct="true"')

    # text
    html_string = re.sub(
        r'^<p>=\s?(.+)<\/p>$',
        """<stringresponse answer="\\1" type="ci">\n<textline size="20"/>\n</stringresponse>""",
        html_string, flags=re.M)

    # explanation
    html_string = html_string.replace("<p>[explanation]\n", """<solution>\n<div class="detailed-solution">\n<p>Explanation</p>\n<p>""")
    html_string = html_string.replace("\n[explanation]</p>", """</p>\n</div>\n</solution>""")

    xml_string = "<problem>\n{}\n</problem>".format(html_string)

    return xml_string.strip()


def xml_to_html(xml_string):
    if not xml_string:
        return ""

    html_string = xml_string
    html_string = html_string.replace('choice', 'label')
    html_string = html_string.replace('false">', 'false"><input name="radio-{}" type="radio"> ')
    html_string = html_string.replace('true">', 'true"><input name="radio-{}" type="radio"> ')

    html_string = html_string.replace('</textline>', '')
    html_string = html_string.replace('textline', 'input type="text"')
    return html_string.strip()


def answer_from_xml(xml_string):
    if not xml_string:
        return ""

    answer = ""
    root = etree.fromstring(xml_string)
    mcp = root.find('multiplechoiceresponse')
    if mcp is not None:
        choicegroup = mcp.find('choicegroup')
        choices = choicegroup.findall('choice')
        for choice in choices:
            if choice.get('correct') == 'true':
                answer = choice.text
                return answer

    sr = root.find('stringresponse')
    if sr is not None:
        answer = sr.get('answer', "")
        return answer

    return answer.strip()

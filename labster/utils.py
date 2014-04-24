from lxml import etree


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
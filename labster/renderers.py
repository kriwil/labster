from django.utils.xmlutils import SimplerXMLGenerator

from rest_framework.compat import StringIO
# from rest_framework.compat import smart_text
from rest_framework.renderers import XMLRenderer


class LabsterXMLRenderer(XMLRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Renders *obj* into serialized XML.
        """
        if data is None:
            return ''

        stream = StringIO()

        root_name = renderer_context.get('root_name', 'root')
        root_attributes = renderer_context.get('root_attributes', {})

        xml = SimplerXMLGenerator(stream, self.charset)
        xml.startDocument()
        xml.startElement(root_name, root_attributes)

        self._to_xml(xml, data)

        xml.endElement(root_name)
        xml.endDocument()
        return stream.getvalue()

    def _to_xml(self, xml, data):
        is_element = all([
            'name' in data,
            'attrib' in data,
            'children' in data,
        ])

        if is_element:
            xml.startElement(data['name'], data['attrib'])
            for each in data['children']:
                self._to_xml(xml, each)
            xml.endElement(data['name'])

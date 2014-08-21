import six
try:
    import cStringIO.StringIO as StringIO
except ImportError:
    StringIO = six.StringIO

from django.http import HttpResponse
from django.shortcuts import render
from django.utils.xmlutils import SimplerXMLGenerator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View


def demo_lab(request):
    template_name = 'labster/lms/demo_lab.html'
    context = {
    }
    return render(request, template_name, context)


class XMLView(View):
    charset = 'utf-8'
    root_name = 'Root'

    def get_root_attributes(self):
        return {}

    def insert_children(self, xml):
        pass

    def get(self, request, *args, **kwargs):

        stream = StringIO()
        xml = SimplerXMLGenerator(stream, self.charset)
        xml.startDocument()
        xml.startElement(self.root_name, self.get_root_attributes())

        self.insert_children(xml)

        xml.endElement(self.root_name)
        xml.endDocument()

        response = HttpResponse(stream.getvalue())
        response['Content-Type'] = 'text/xml; charset={}'.format(self.charset)

        return response


class SettingsXml(XMLView):
    root_name = 'Settings'

    def get_root_attributes(self):
        return {
            'EngineXML': "Engine_Cytogenetics.xml",
            'NavigationMode': "Classic",
            'CameraMode': "Standard",
            'InputMode': "Mouse",
            'HandMode': "Hand",
            'URLPrefix': "http://s3-us-west-2.amazonaws.com/labster/unity/",
        }


class PlatformXml(XMLView):
    root_name = 'Settings'

    def get_root_attributes(self):
        return {
            'Id': "ModularLab",
            'Version': "1",
            'Title': "Labster",
            'LoaderAsset': "FlaskLoadingScene",
            'LoaderScene': "FlaskLoadingScene",
        }


class ServerXml(XMLView):
    root_name = 'Server'

    def get_root_attributes(self):
        return {
            'Url': "",
        }

    def insert_children(self, xml):
        game_progress = "/labster/api/collect-response/gameprogress/"
        device_info = "/labster/api/collect-response/deviceinfo/"
        quiz_statistic = "/labster/api/collect-response/quizstatistic/"
        save_game = "/labster/api/collect-response/savegame/"
        send_email = "/labster/api/collect-response/sendemail/"
        player_start_end = "/labster/api/collect-response/playerstartend/"
        children = [
            {'Id': "GameProgress", 'Path': game_progress},
            {'Id': "DeviceInfo", 'Path': device_info},
            {'Id': "QuizStatistic", 'Path': quiz_statistic},
            {'Id': "SaveGame", 'Path': save_game},
            {'Id': "SendEmail", 'Path': send_email},
            {'Id': "PlayerStartEnd", 'Path': player_start_end},
        ]

        for child in children:
            xml.startElement('ServerAPI', child)
            xml.endElement('ServerAPI')


settings_xml = SettingsXml.as_view()
server_xml = ServerXml.as_view()
platform_xml = PlatformXml.as_view()


@csrf_exempt
def collect_response(request, api_type):
    print api_type
    print request.POST
    return HttpResponse('')

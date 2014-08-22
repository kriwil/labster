import six
try:
    import cStringIO.StringIO as StringIO
except ImportError:
    StringIO = six.StringIO

from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.xmlutils import SimplerXMLGenerator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from rest_framework.authtoken.models import Token

from labster.models import LabProxy


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


class LabProxyXMLView(XMLView):

    def get_lab_proxy(self):
        from opaque_keys.edx.locations import SlashSeparatedCourseKey

        course_id = self.kwargs.get('course_id')
        section = self.kwargs.get('section')

        course_key = SlashSeparatedCourseKey.from_deprecated_string(course_id)
        location = "i4x://{}/{}/sequential/{}".format(
            course_key.org, course_key.course, section)

        lab_proxy = LabProxy.objects.get(location=location)
        return lab_proxy


class SettingsXml(LabProxyXMLView):
    root_name = 'Settings'

    def get_root_attributes(self):
        engine_xml = "Engine_Cytogenetics.xml"
        lab_proxy = self.get_lab_proxy()
        if lab_proxy.lab.engine_xml:
            engine_xml = lab_proxy.lab.engine_xml
            # engine_xml = "http://192.168.4.45:9000/unity/1408688971_4.zip"

        return {
            'EngineXML': engine_xml,
            'NavigationMode': "Classic",
            'CameraMode': "Standard",
            'InputMode': "Mouse",
            'HandMode': "Hand",
            'URLPrefix': "http://s3-us-west-2.amazonaws.com/labster/unity/",
            # 'URLPrefix': "http://192.168.4.45:9000/unity/",
        }


class PlatformXml(LabProxyXMLView):
    root_name = 'Settings'

    def get_root_attributes(self):
        return {
            'Id': "ModularLab",
            'Version': "1",
            'Title': "Labster",
            'LoaderAsset': "FlaskLoadingScene",
            'LoaderScene': "FlaskLoadingScene",
        }


class ServerXml(LabProxyXMLView):
    root_name = 'Server'

    def get_root_attributes(self):
        return {
            'Url': "",
        }

    def insert_children(self, xml):
        lab_proxy = self.get_lab_proxy()

        # save_game = "/labster/api/collect-response/savegame/"
        quiz_statistic = "/labster/api/collect-response/quizstatistic/"
        game_progress = "/labster/api/collect-response/gameprogress/"
        device_info = "/labster/api/collect-response/deviceinfo/"
        send_email = "/labster/api/collect-response/sendemail/"
        player_start_end = "/labster/api/collect-response/playerstartend/"

        token, _ = Token.objects.get_or_create(user=self.request.user)
        save_game = reverse('labster-api:save', args=[lab_proxy.lab_id])
        save_game = "{}?token={}".format(save_game, token.key)

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
    if api_type == 'savegame':
        messages = [
            str(request.user),
            api_type,
            str(request.POST),
            str(request.FILES),
        ]
        message = "\n----\n".join(messages)
        send_mail('DEBUG: {}'.format(api_type), message, 'log@example.com',
                ['kriwil+debug@gmail.com'], fail_silently=True)
    return HttpResponse('')

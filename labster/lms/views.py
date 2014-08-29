import six
try:
    import cStringIO.StringIO as StringIO
except ImportError:
    StringIO = six.StringIO

from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.xmlutils import SimplerXMLGenerator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from labster.models import LabProxy, UserSave, UserAttempt


URL_PREFIX = getattr(settings, 'LABSTER_UNITY_URL_PREFIX', '')


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
        user = self.request.user

        if lab_proxy.lab.engine_xml:
            engine_xml = lab_proxy.lab.engine_xml

        # check if user has finished
        # if user's not finished the game, try to fetch the save file
        user_attempt = UserAttempt.objects.latest_for_user(lab_proxy, user)
        if user_attempt and not user_attempt.is_finished:
            # check for save game
            try:
                user_save = UserSave.objects.get(lab_proxy=lab_proxy, user=user)
            except UserSave.DoesNotExist:
                pass
            else:
                if user_save.save_file:
                    engine_xml = user_save.save_file.url

        return {
            'EngineXML': engine_xml,
            'NavigationMode': "Classic",
            'CameraMode': "Standard",
            'InputMode': "Mouse",
            'HandMode': "Hand",
            'URLPrefix': URL_PREFIX,
            # 'URLPrefix': "http://192.168.4.45:9000/unity/",
        }


class PlatformXml(LabProxyXMLView):
    root_name = 'Settings'

    def get_root_attributes(self):
        return {
            'Id': "ModularLab",
            'Version': "1",
            'Title': "Labster",
            'LoaderAsset': "Loading",
            'LoaderScene': "Loading",
        }


class ServerXml(LabProxyXMLView):
    root_name = 'Server'

    def get_root_attributes(self):
        return {
            # 'Url': "http://localhost:8000",
            'Url': "https://edx.labster.com",
        }

    def insert_children(self, xml):
        lab_proxy = self.get_lab_proxy()

        # save_game = "/labster/api/collect-response/savegame/"
        # player_start_end = "/labster/api/collect-response/playerstartend/"
        # wiki = "/labster/api/collect-response/Wiki/"
        # quiz_statistic = "/labster/api/collect-response/QuizStatistic/"
        # game_progress = "/labster/api/collect-response/GameProgress/"
        # device_info = "/labster/api/collect-response/DeviceSnfo/"
        # send_email = "/labster/api/collect-response/SendEmail/"

        save_game = reverse('labster-api:save', args=[lab_proxy.id])
        player_start_end = reverse('labster-api:play', args=[lab_proxy.id])
        quiz_block = reverse('labster-api:questions', args=[lab_proxy.id])
        quiz_statistic = reverse('labster-api:create-log', args=[lab_proxy.id, 'QuizStatistic'])
        game_progress = reverse('labster-api:create-log', args=[lab_proxy.id, 'GameProgress'])
        device_info = reverse('labster-api:create-log', args=[lab_proxy.id, 'DeviceInfo'])
        send_email = reverse('labster-api:create-log', args=[lab_proxy.id, 'SendEmail'])

        # wiki = reverse('labster-api:wiki-article', args=['replaceme'])
        wiki = "/labster/api/wiki/article/"

        children = [
            {'Id': "GameProgress", 'Path': game_progress},
            {'Id': "DeviceInfo", 'Path': device_info},
            {'Id': "QuizStatistic", 'Path': quiz_statistic},
            {'Id': "SaveGame", 'Path': save_game},
            {'Id': "SendEmail", 'Path': send_email},
            {'Id': "PlayerStartEnd", 'Path': player_start_end},
            {'Id': "Wiki", 'Path': wiki, 'CatchError': "false"},
            {'Id': "QuizBlock", 'Path': quiz_block},
        ]

        for child in children:
            xml.startElement('ServerAPI', child)
            xml.endElement('ServerAPI')


settings_xml = SettingsXml.as_view()
server_xml = ServerXml.as_view()
platform_xml = PlatformXml.as_view()


@csrf_exempt
def collect_response(request, api_type):
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

import six
try:
    import cStringIO.StringIO as StringIO
except ImportError:
    StringIO = six.StringIO

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.xmlutils import SimplerXMLGenerator
from django.views.generic import View

from labster.models import LabProxy, UserSave, UserAttempt


URL_PREFIX = getattr(settings, 'LABSTER_UNITY_URL_PREFIX', '')
API_PREFIX = getattr(settings, 'LABSTER_UNITY_API_PREFIX', '')


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

    def get_engine_xml(self, lab_proxy, user):
        engine_xml = "Engine_Cytogenetics.xml"

        if lab_proxy.lab.engine_xml:
            engine_xml = lab_proxy.lab.engine_xml

        user_save_file_url = self.get_user_save_file_url(lab_proxy, user)
        if user_save_file_url:
            engine_xml = user_save_file_url

        return engine_xml

    def get_user_save_file_url(self, lab_proxy, user):
        engine_xml = ''

        # check if user has finished
        # if user's not finished the game, try to fetch the save file
        user_attempt = UserAttempt.objects.latest_for_user(lab_proxy, user)
        if not user_attempt or user_attempt.is_finished:
            return ''

        # check for save game
        try:
            user_save = UserSave.objects.get(lab_proxy=lab_proxy, user=user)
        except UserSave.DoesNotExist:
            pass
        else:
            if user_save.save_file:
                engine_xml = user_save.save_file.url

        return engine_xml

    def get_root_attributes(self):
        lab_proxy = self.get_lab_proxy()
        user = self.request.user

        engine_xml = self.get_engine_xml(lab_proxy, user)

        return {
            'EngineXML': engine_xml,
            'NavigationMode': "Classic",
            'CameraMode': "Standard",
            'InputMode': "Mouse",
            'HandMode': "Hand",
            'URLPrefix': URL_PREFIX,
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
            'Url': API_PREFIX,
        }

    def insert_children(self, xml):
        lab_proxy = self.get_lab_proxy()

        save_game = reverse('labster-api:save', args=[lab_proxy.id])
        player_start_end = reverse('labster-api:play', args=[lab_proxy.id])
        quiz_block = reverse('labster-api:questions', args=[lab_proxy.id])

        if lab_proxy.lab.use_quiz_blocks:
            quiz_statistic = reverse('labster-api:answer', args=[lab_proxy.id])
        else:
            quiz_statistic = reverse('labster-api:create-log', args=[lab_proxy.id, 'quiz_statistic'])

        game_progress = reverse('labster-api:create-log', args=[lab_proxy.id, 'game_progress'])
        device_info = reverse('labster-api:create-log', args=[lab_proxy.id, 'device_info'])
        send_email = reverse('labster-api:create-log', args=[lab_proxy.id, 'send_email'])

        # wiki = reverse('labster-api:wiki-article', args=['replaceme'])
        wiki = "/labster/api/wiki/article/"

        children = [
            {'Id': "GameProgress", 'Path': game_progress},
            {'Id': "DeviceInfo", 'Path': device_info},
            {'Id': "QuizStatistic", 'Path': quiz_statistic},
            {'Id': "SaveGame", 'Path': save_game},
            {'Id': "SendEmail", 'Path': send_email},
            {'Id': "PlayerStartEnd", 'Path': player_start_end},
            {'Id': "Wiki", 'Path': wiki, 'CatchError': "false", 'AllowCache': "true"},
            {'Id': "QuizBlock", 'Path': quiz_block},
        ]

        for child in children:
            xml.startElement('ServerAPI', child)
            xml.endElement('ServerAPI')



class StartNewLab(View):

    def get(self, request, *args, **kwargs):
        pass


settings_xml = SettingsXml.as_view()
server_xml = ServerXml.as_view()
platform_xml = PlatformXml.as_view()

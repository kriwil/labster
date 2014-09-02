import json
from lxml import etree

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.uploadhandler import StopFutureHandlers
from django.http import Http404
from django.http import QueryDict
from django.http.multipartparser import parse_header, ChunkIter
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ParseError
from rest_framework.generics import ListCreateAPIView, CreateAPIView
from rest_framework.parsers import DataAndFiles
from rest_framework.parsers import FormParser, MultiPartParser, BaseParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import XMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from labster.api.serializers import (
    ErrorInfoSerializer, DeviceInfoSerializer,
    UserAttemptSerializer, FinishLabSerializer)
from labster.authentication import GetTokenAuthentication
from labster.models import (
    UserSave, ErrorInfo, DeviceInfo, LabProxy, UserAttempt, UnityLog)
from labster.parsers.problem_parsers import MultipleChoiceProblemParser
from labster.renderers import LabsterXMLRenderer


def invoke_xblock_handler(*args, **kwargs):
    from courseware.module_render import _invoke_xblock_handler

    """
    Wrapper so it could be mocked
    """
    return _invoke_xblock_handler(*args, **kwargs)


def get_usage_key():
    from opaque_keys.edx.keys import UsageKey
    return UsageKey


def get_modulestore():
    from xmodule.modulestore.django import modulestore
    return modulestore


def get_lab_by_location(location):
    UsageKey = get_usage_key()
    modulestore = get_modulestore()

    locator = UsageKey.from_string(location)
    descriptor = modulestore().get_item(locator)
    lab_id = descriptor.lab_id
    lab = {}

    quiz_blocks = []
    for _quiz_block in descriptor.get_children():
        problems = []
        for _problem in _quiz_block.get_children():
            problem = {
                'id': unicode(_problem.location),
                'content': _problem.data,
                'platform_xml': _problem.platform_xml,
                'tags': _problem.tags,
            }

            problems.append(problem)

        quiz_block = {
            'id': unicode(_quiz_block.location),
            'slug': _quiz_block.display_name,
            'problems': problems,
        }

        quiz_blocks.append(quiz_block)

    lab.update({
        'lab': {
            'id': int(lab_id),
            'quiz_blocks': quiz_blocks,
        }
    })

    return lab


def parse_platform_xml(xml_string):
    quiz_tree = etree.fromstring(xml_string)
    quiz_element = {
        'name': quiz_tree.tag,
        'attrib': quiz_tree.attrib,
        'children': [],
    }

    for options_tree in quiz_tree.getchildren():
        options_element = {
            'name': options_tree.tag,
            'attrib': options_tree.attrib,
            'children': [],
        }

        for option_tree in options_tree.getchildren():
            options_element['children'].append(
                {
                    'name': option_tree.tag,
                    'attrib': option_tree.attrib,
                    'children': [],
                }
            )

        quiz_element['children'].append(options_element)

    return quiz_element


def parse_edx_xml(xml_string, problem_id):
    parsed_problem = MultipleChoiceProblemParser(xml_string)

    options = parsed_problem.options
    options_element = {
        'name': "Options",
        'attrib': {},
        'children': [],
    }

    for each in options:
        attrib = {'Sentence': each['text']}
        if each['is_correct']:
            attrib['IsCorrectAnswer'] = "true"
        option = {
            'name': "Option",
            'attrib': attrib,
            'children': [],
        }
        options_element['children'].append(option)

    quiz_element = {
        'name': "Quiz",
        'attrib': {
            'Id': problem_id,
            'Sentence': str(parsed_problem.problem).encode('string_escape'),
            'CorrectMessage': str(parsed_problem.solution).encode('string_escape'),
            'WrongMessage': "No. This is incorrect - please try again!",
        },
        'children': [options_element],
    }

    return quiz_element


def get_lab_by_location_for_xml(location):
    lab_by_location = get_lab_by_location(location)

    response_data = {
        'name': "QuizBlocks",
        'attrib': {},
        'children': [],
    }

    for quiz_block in lab_by_location['lab']['quiz_blocks']:
        qb_element = {
            'name': "QuizBlock",
            'attrib': {
                'Id': quiz_block['slug'],
            },
            'children': [],
            'children_tree': [],
        }

        for problem in quiz_block['problems']:
            if problem['platform_xml']:
                quiz_element = parse_platform_xml(problem['platform_xml'])
            else:
                quiz_element = parse_edx_xml(problem['content'], problem['id'])

            qb_element['children'].append(quiz_element)

        response_data['children'].append(qb_element)

    return response_data


class RendererMixin:
    renderer_classes = (XMLRenderer, JSONRenderer)
    charset = 'utf-8'


class LabsterRendererMixin(object):
    renderer_classes = (LabsterXMLRenderer,)
    charset = 'utf-8'

    def get_labster_renderer_context(self):
        return {}

    def get_renderer_context(self):
        ctx = super(LabsterRendererMixin, self).get_renderer_context()
        ctx.update(self.get_labster_renderer_context())
        return ctx


class ParserMixin:
    parser_classes = (FormParser, MultiPartParser,)


class AuthMixin:
    authentication_classes = (TokenAuthentication, SessionAuthentication, GetTokenAuthentication)
    permission_classes = (IsAuthenticated,)


class APIRoot(RendererMixin, AuthMixin, APIView):

    def get(self, request, *args, **kwargs):
        format = kwargs.get('format')
        lab_proxy_detail_url = reverse(
            'labster-api:questions',
            request=request,
            kwargs={'lab_id': 'LAB-ID'},
            format=format)

        answer_problem_url = reverse(
            'labster-api:answer-problem',
            request=request,
            kwargs={'lab_id': 'LAB-ID'},
            format=format)

        save_url = reverse(
            'labster-api:save',
            request=request,
            kwargs={'lab_id': 'LAB-ID'},
            format=format)

        error_url = reverse(
            'labster-api:log-error',
            request=request,
            kwargs={'lab_id': 'LAB-ID'},
            format=format)

        device_url = reverse(
            'labster-api:log-device',
            request=request,
            kwargs={'lab_id': 'LAB-ID'},
            format=format)

        return Response({
            'questions': lab_proxy_detail_url,
            'answer-problem': answer_problem_url,
            'save': save_url,
            'error': error_url,
            'device': device_url,
        })


class UserAuth(RendererMixin, APIView):

    def post(self, request, *args, **kwargs):
        email = request.DATA.get('email')
        password = request.DATA.get('password')
        response_data = {}
        http_status = status.HTTP_200_OK

        if not email or not password:
            response_data['status'] = False

        else:
            try:
                user = User.objects.get(email=email)
            except:
                response_data['status'] = False
            else:
                response_data['status'] = user.check_password(password)

        if response_data['status']:
            token, _ = Token.objects.get_or_create(user=user)
            response_data.update({
                'user_id': user.id,
                'token': token.key,
            })

        else:
            http_status = status.HTTP_400_BAD_REQUEST

        return Response(response_data, status=http_status)


class CustomFileUploadParser(BaseParser):
    """
    Parser for file upload data.
    """
    media_type = 'multipart/form-data'

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Returns a DataAndFiles object.

        `.data` will be None (we expect request body to be a file content).
        `.files` will be a `QueryDict` containing one 'file' element.
        """

        parser_context = parser_context or {}
        request = parser_context['request']
        encoding = parser_context.get('encoding', settings.DEFAULT_CHARSET)
        meta = request.META
        upload_handlers = request.upload_handlers
        filename = self.get_filename(stream, media_type, parser_context)

        # Note that this code is extracted from Django's handling of
        # file uploads in MultiPartParser.
        content_type = meta.get('HTTP_CONTENT_TYPE',
                                meta.get('CONTENT_TYPE', ''))
        try:
            content_length = int(meta.get('HTTP_CONTENT_LENGTH',
                                          meta.get('CONTENT_LENGTH', 0)))
        except (ValueError, TypeError):
            content_length = None

        if not filename:
            filename = 'autosave.zip'

        # See if the handler will want to take care of the parsing.
        for handler in upload_handlers:
            result = handler.handle_raw_input(None,
                                              meta,
                                              content_length,
                                              None,
                                              encoding)
            if result is not None:
                return DataAndFiles(None, {'file': result[1]})

        # This is the standard case.
        possible_sizes = [x.chunk_size for x in upload_handlers if x.chunk_size]
        chunk_size = min([2 ** 31 - 4] + possible_sizes)
        chunks = ChunkIter(stream, chunk_size)
        counters = [0] * len(upload_handlers)

        for handler in upload_handlers:
            try:
                handler.new_file(None, filename, content_type,
                                 content_length, encoding)
            except StopFutureHandlers:
                break

        for chunk in chunks:
            for i, handler in enumerate(upload_handlers):
                chunk_length = len(chunk)
                chunk = handler.receive_data_chunk(chunk, counters[i])
                counters[i] += chunk_length
                if chunk is None:
                    break

        for i, handler in enumerate(upload_handlers):
            file_obj = handler.file_complete(counters[i])
            if file_obj:
                return DataAndFiles(None, {'file': file_obj})
        raise ParseError("FileUpload parse error - "
                         "none of upload handlers can handle the stream")

    def get_filename(self, stream, media_type, parser_context):
        """
        Detects the uploaded file name. First searches a 'filename' url kwarg.
        Then tries to parse Content-Disposition header.
        """
        try:
            return parser_context['kwargs']['filename']
        except KeyError:
            pass

        try:
            meta = parser_context['request'].META
            disposition = parse_header(meta['HTTP_CONTENT_DISPOSITION'])
            return disposition[1]['filename']
        except (AttributeError, KeyError):
            pass


class CreateSave(AuthMixin, APIView):
    parser_classes = (CustomFileUploadParser,)

    def get_root_attributes(self):
        file_url = ""
        # if self.user_save:
        #     file_url = self.user_save.save_file.url
        return {
            'FileUrl': file_url,
        }

    def get_labster_renderer_context(self):
        return {
            'root_name': "Save",
            'root_attributes': self.get_root_attributes(),
        }

    def get(self, request, *args, **kwargs):
        # http://www.django-rest-framework.org/api-guide/requests#user
        user = request.user
        lab_id = kwargs.get('lab_id')
        http_status = status.HTTP_200_OK

        try:
            lab_proxy = LabProxy.objects.get(id=lab_id)
            self.user_save = UserSave.objects.get(lab_proxy_id=lab_proxy.id, user_id=user.id)
        except (LabProxy.DoesNotExist, UserSave.DoesNotExist):
            http_status = status.HTTP_404_NOT_FOUND

        response_data = {}
        return Response(response_data, status=http_status)

    def pre_save(self, obj):
        obj.user = self.request.user
        lab_id = self.kwargs.get('lab_id')
        obj.lab_proxy = get_object_or_404(LabProxy, id=lab_id)

    def post(self, request, *args, **kwargs):
        user = request.user
        lab_id = kwargs.get('lab_id')

        lab_proxy = get_object_or_404(LabProxy, id=lab_id)
        self.user_save, _ = UserSave.objects.get_or_create(user=user, lab_proxy=lab_proxy)

        http_status = status.HTTP_200_OK

        file_name = self.user_save.get_new_save_file_name()
        # data_file = request.FILES.get('file')
        # self.user_save.save_file.save(SimpleUploadedFile(file_name, data_file.read().strip()))
        try:
            self.user_save.save_file.save(SimpleUploadedFile(file_name, request.body.strip()))
            self.user_save.save()
        except:
            pass

        return Response({}, status=http_status)


class PlayLab(RendererMixin, ParserMixin, AuthMixin, ListCreateAPIView):

    def get(self, request, *args, **kwargs):
        # http://www.django-rest-framework.org/api-guide/requests#user
        user = request.user
        lab_id = kwargs.get('lab_id')

        lab_proxy = get_object_or_404(LabProxy, id=lab_id)
        user_attempt = UserAttempt.objects.latest_for_user(lab_proxy, user)
        if not user_attempt:
            raise Http404

        serializer = UserAttemptSerializer(user_attempt)
        return Response(serializer.data)

    def pre_save(self, obj, data=None):
        obj.user = self.request.user
        obj.lab_proxy = get_object_or_404(LabProxy, id=self.kwargs.get('lab_id'))

        if obj.is_finished and data.get('play') == '1':
            obj.play_count += 1
            obj.is_finished = False

    def post(self, request, *args, **kwargs):
        data = request.DATA.copy()

        user = request.user
        lab_id = kwargs.get('lab_id')
        lab_proxy = get_object_or_404(LabProxy, id=lab_id)

        user = get_object_or_404(User, id=user.id)
        data.update({
            'user': user,
            'lab_proxy': lab_proxy,
        })

        serializer = UserAttemptSerializer(data=data)
        if serializer.is_valid():
            self.pre_save(serializer.object, data=data)
            serializer.save()
            http_status = status.HTTP_201_CREATED
            return Response(serializer.data, status=http_status)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FinishLab(RendererMixin, ParserMixin, AuthMixin, ListCreateAPIView):

    def get(self, request, *args, **kwargs):
        # http://www.django-rest-framework.org/api-guide/requests#user
        user = request.user

        lab_id = kwargs.get('lab_id')
        lab_proxy = get_object_or_404(LabProxy, id=lab_id)

        user_attempt = UserAttempt.objects.latest_for_user(lab_proxy, user)
        if not user_attempt:
            raise Http404

        serializer = FinishLabSerializer(user_attempt)
        return Response(serializer.data)

    def pre_save(self, obj, data=None):
        obj.user = self.request.user
        lab_id = self.kwargs.get('lab_id')
        obj.lab_proxy = get_object_or_404(LabProxy, id=lab_id)

    def post(self, request, *args, **kwargs):
        data = request.DATA

        user = request.user
        lab_id = kwargs.get('lab_id')
        lab_proxy = get_object_or_404(LabProxy, id=lab_id)

        user = get_object_or_404(User, id=user.id)
        user_attempt = UserAttempt.objects.latest_for_user(lab_proxy, user)
        if not user_attempt:
            raise Http404

        serializer = FinishLabSerializer(instance=user_attempt, data=data)
        if serializer.is_valid():
            self.pre_save(serializer.object, data=data)
            serializer.save()
            http_status = status.HTTP_204_NO_CONTENT
            return Response(serializer.data, status=http_status)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LabSettings(LabsterRendererMixin, AuthMixin, APIView):

    def get_root_attributes(self):
        return {
            'EngineXML': "",
            'NavigationNode': "Classic",
            'CameraMode': "Standard",
            'InputMode': "Mouse",
            'DebugOculus': "true",
            'OuputDebugLog': "true",
        }

    def get_labster_renderer_context(self):
        return {
            'root_name': "Settings",
            'root_attributes': self.get_root_attributes(),
        }

    def get(self, request, *args, **kwargs):
        response_data = {}
        return Response(response_data, status=status.HTTP_200_OK)


class CreateError(LabsterRendererMixin, ParserMixin, AuthMixin, CreateAPIView):
    model = ErrorInfo
    serializer_class = ErrorInfoSerializer

    def get_labster_renderer_context(self):
        return {
            'root_name': "Error",
            'root_attributes': {},
        }

    def pre_save(self, obj):
        obj.user = self.request.user
        lab_id = self.kwargs.get('lab_id')
        obj.lab_proxy = get_object_or_404(LabProxy, id=lab_id)


class CreateDevice(LabsterRendererMixin, ParserMixin, AuthMixin, CreateAPIView):
    model = DeviceInfo
    serializer_class = DeviceInfoSerializer

    def get_labster_renderer_context(self):
        return {
            'root_name': "Device",
            'root_attributes': {},
        }

    def pre_save(self, obj):
        obj.user = self.request.user
        lab_id = self.kwargs.get('lab_id')
        obj.lab_proxy = get_object_or_404(LabProxy, id=lab_id)


class LabProxyView(LabsterRendererMixin, AuthMixin, APIView):

    def get_root_attributes(self):
        return {
            'Id': self.kwargs.get('lab_id'),
        }

    def get_labster_renderer_context(self):
        return {
            'root_name': "Lab",
            'root_attributes': self.get_root_attributes(),
        }

    def get_response_data(self, lab_id):
        lab_proxy = get_object_or_404(LabProxy, id=lab_id)
        return get_lab_by_location_for_xml(lab_proxy.location)

    def get(self, request, format=None, *args, **kwargs):
        lab_id = kwargs.get('lab_id')
        response_data = self.get_response_data(lab_id)
        return Response(response_data)

    def post(self, request, format=None, *args, **kwargs):
        lab_id = kwargs.get('lab_id')
        response_data = self.get_response_data(lab_id)
        return Response(response_data)


class WikiMixin(object):
    def get_root_attributes(self):
        return {
            'id': self.article_id,
            'title': self.title,
            'slug': self.slug,
        }

    def get_labster_renderer_context(self):
        return {
            'root_name': "Wiki",
            'root_attributes': self.get_root_attributes(),
        }

    def get_response_data(self):
        # ref:
        # https://github.com/Bodekaer/Labster.EdX.django-wiki/blob/66f357e4f6db1b96006ed8e75cd867f7541bb812/wiki/models/article.py#L178
        content_markdown = self.article.current_revision.content

        return {
            'name': "Content",
            'attrib': {},
            'children': [
                {
                    'name': "HTML",
                    'attrib': {},
                    'children': [],
                    'text': self.article.render(),
                },
                {
                    'name': "Markdown",
                    'attrib': {},
                    'children': [],
                    'text': content_markdown,
                }
            ]
        }


class Wiki(WikiMixin, LabsterRendererMixin, APIView):

    def get(self, request, course_id, *args, **kwargs):
        from course_wiki.utils import course_wiki_slug
        from courseware.courses import get_course_by_id
        from opaque_keys.edx.locations import SlashSeparatedCourseKey
        from wiki.models import URLPath, Article

        try:
            # ref:
            # https://github.com/Bodekaer/Labster.EdX/blob/cfcbdc01453150f1025e59c9b6a9a03ace390f4a/lms/djangoapps/course_wiki/views.py#L39
            course = get_course_by_id(SlashSeparatedCourseKey.from_deprecated_string(course_id))
        except ValueError:
            raise Http404

        course_slug = course_wiki_slug(course)

        url_path = URLPath.get_by_path(course_slug, select_related=True)

        try:
            article = Article.objects.get(id=url_path.article.id)
        except Article.DoesNotExist:
            article = None

        self.article_id = str(url_path.article.id)
        self.slug = course_slug
        self.title = unicode(article)
        self.article = article

        response_data = self.get_response_data()
        return Response(response_data)


class ArticleSlug(WikiMixin, LabsterRendererMixin, APIView):

    def get(self, request, article_slug, *args, **kwargs):
        from wiki.models import URLPath, Article

        # since we already have article slug we don't need to search the course
        # article slug is unique
        try:
            url_path = URLPath.get_by_path(article_slug, select_related=True)
        except ObjectDoesNotExist:
            raise Http404

        try:
            article = Article.objects.get(id=url_path.article.id)
        except Article.DoesNotExist:
            article = None

        self.article_id = str(url_path.article.id)
        self.slug = article_slug
        self.title = unicode(article)
        self.article = article

        response_data = self.get_response_data()
        return Response(response_data)


class AnswerProblem(RendererMixin, ParserMixin, AuthMixin, APIView):

    def __init__(self, *args, **kwargs):
        self.usage_key = get_usage_key()
        self.modulestore = get_modulestore()
        super(AnswerProblem, self).__init__(*args, **kwargs)

    def get_problem_locator_descriptor(self, problem_id):
        locator = self.usage_key.from_string(problem_id)
        descriptor = self.modulestore().get_item(locator)

        return locator, descriptor

    def get_post_data(self, request, problem_locator, answer, time_spent):

        request.POST = request.POST.copy()
        field_name = "input_{tag}-{org}-{course}-{category}-{name}_2_1"
        field_key = {
            'tag': problem_locator.tag,
            'org': problem_locator.org,
            'course': problem_locator.course,
            'category': problem_locator.category,
            'name': problem_locator.name,
        }

        field = field_name.format(**field_key)
        post_data = QueryDict('', mutable=True)
        post_data[field] = answer
        post_data['time_spent'] = time_spent

        return post_data

    def call_xblock_handler(self, request, location, problem_locator, answer, time_spent):

        locator = self.usage_key.from_string(location)
        course_id = locator.course_key.to_deprecated_string()
        usage_id = problem_locator.to_deprecated_string()
        usage_id = usage_id.replace('/', ';_')
        handler = 'xmodule_handler'
        suffix = 'problem_check'
        user = request.user
        request.POST = self.get_post_data(request, problem_locator, answer, time_spent)

        return invoke_xblock_handler(request, course_id, usage_id, handler, suffix, user)

    def post(self, request, *args, **kwargs):
        response_data = {}

        lab_id = kwargs.get('lab_id')
        problem_id = request.DATA.get('problem')
        answer = request.DATA.get('answer')
        time_spent = request.DATA.get('time_spent')

        problem_locator, problem_descriptor = self.get_problem_locator_descriptor(problem_id)

        if 'multiplechoiceresponse' in problem_descriptor.data:
            answer = "choice_{}".format(answer)

        result = self.call_xblock_handler(request, lab_id, problem_locator, answer, time_spent)
        content = json.loads(result.content)
        response_data = {
            'correct': content.get('success') == 'correct',
        }

        return Response(response_data, status=status.HTTP_201_CREATED)


class UnityPlayLab(ParserMixin, AuthMixin, APIView):

    def post(self, request, *args, **kwargs):
        lab_id = kwargs.get('lab_id')
        lab_proxy = get_object_or_404(LabProxy, id=lab_id)

        start_end_type = request.POST.get('StartEndType')
        try:
            start_end_type = int(start_end_type)
        except TypeError:
            return Response('', status=status.HTTP_400_BAD_REQUEST)
        else:
            if start_end_type not in [1, 2]:
                return Response('', status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        if start_end_type == 1:
            user_attempt = UserAttempt.objects.create(
                lab_proxy=lab_proxy, user=user)
        else:
            user_attempt = UserAttempt.objects.latest_for_user(lab_proxy, user)
            user_attempt.is_finished = True
            user_attempt.save()

        response_data = ''

        return Response(response_data, status=status.HTTP_204_NO_CONTENT)


class CreateLog(ParserMixin, AuthMixin, APIView):

    def post(self, request, *args, **kwargs):
        log_type = kwargs.get('log_type')
        lab_id = kwargs.get('lab_id')

        lab_proxy = get_object_or_404(LabProxy, id=lab_id)
        user = request.user
        message = request.POST.copy()
        url = request.build_absolute_uri()
        request_method = request.method

        UnityLog.new(user, lab_proxy,
                     log_type, message, url, request_method)
        return Response('', status=status.HTTP_204_NO_CONTENT)

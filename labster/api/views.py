from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser

from labster.api.serializers import LabSerializer, LabProxySerializer, ProblemSerializer, UserSaveSerializer
from labster.models import Lab, QuizBlock, Problem, LabProxy, UserSave, ErrorInfo, DeviceInfo
from labster.models import create_lab_proxy, update_lab_proxy, create_user_save, UserProblem, UserLabProxy


class LabList(ListAPIView):
    model = Lab
    queryset = Lab.objects.all()
    serializer_class = LabSerializer


class LabDetail(RetrieveAPIView):
    model = Lab
    queryset = Lab.objects.all()
    serializer_class = LabSerializer


class QuizBlockList(ListAPIView):
    model = QuizBlock
    queryset = QuizBlock.objects.all()


class QuizBlockDetail(RetrieveAPIView):
    model = QuizBlock
    queryset = QuizBlock.objects.all()


class ProblemList(ListCreateAPIView):
    model = Problem
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer


class ProblemDetail(RetrieveUpdateDestroyAPIView):
    model = Problem
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer


class LabProxyList(ListCreateAPIView):
    model = LabProxy
    queryset = LabProxy.objects.all()
    serializer_class = LabProxySerializer

    def create(self, request, *args, **kwargs):
        lab_id = request.DATA.get('lab_id')
        location_id = request.DATA.get('location_id')
        lab_proxy_id = request.DATA.get('lab_proxy_id')

        if lab_proxy_id:
            lab_proxy = update_lab_proxy(lab_proxy_id, lab_id)
        else:
            lab_proxy = create_lab_proxy(lab_id, location_id)

        serializer = LabProxySerializer(lab_proxy)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LabProxyDetail(RetrieveAPIView):
    model = LabProxy
    queryset = LabProxy.objects.all()
    serializer_class = LabProxySerializer


class CreateUserProblem(APIView):

    def post(self, request, *args, **kwargs):
        data = request.DATA

        user_id = data.get('user_id')
        problem_id = data.get('problem_id')
        answer = data.get('answer', "").strip()

        # user = User.objects.get(email='staff@example.com')
        user = get_object_or_404(User, id=user_id)
        problem = get_object_or_404(Problem, id=problem_id)

        user_problem = UserProblem.objects.create(problem=problem, user=user, answer=answer)
        user_lab_proxy, created = UserLabProxy.objects.get_or_create(
            user=user, lab_proxy=problem.quiz_block.lab_proxy)

        score = user_lab_proxy.get_user_score()

        response = {
            'is_correct': user_problem.is_correct,
            'score': score,
        }
        return Response(response, status=status.HTTP_201_CREATED)


class CreateUserLabProxy(APIView):

    def get(self, request, *args, **kwargs):
        user_id = request.GET.get('user_id')
        lab_proxy_id = request.GET.get('lab_proxy_id')

        user_lab_proxy = get_object_or_404(UserLabProxy, lab_proxy_id=lab_proxy_id, user_id=user_id)
        response = {
            'id': user_lab_proxy.id,
            'completed': user_lab_proxy.completed,
        }
        return Response(response)

    def post(self, request, *args, **kwargs):
        data = request.DATA

        user_id = data.get('user_id')
        lab_proxy_id = data.get('lab_proxy_id')
        completed = data.get('completed', False)

        user = get_object_or_404(User, id=user_id)
        lab_proxy = get_object_or_404(LabProxy, id=lab_proxy_id)

        user_lab_proxy, created = UserLabProxy.objects.get_or_create(
            user=user, lab_proxy=lab_proxy, defaults={'completed': completed})
        if not user_lab_proxy.completed:
            user_lab_proxy.completed = True
            user_lab_proxy.save()

        response = {
            'user_lab_proxy_id': user_lab_proxy.id,
            'completed': user_lab_proxy.completed,
        }

        http_status = status.HTTP_201_CREATED if created else status.HTTP_204_NO_CONTENT
        return Response(response, status=http_status)


class CreateUserSave(APIView):

    def get(self, request, *args, **kwargs):
        user_id = request.GET.get('user_id')
        lab_proxy_id = request.GET.get('lab_proxy_id')

        user_save = get_object_or_404(UserSave, lab_proxy_id=lab_proxy_id, user_id=user_id)
        serializer = UserSaveSerializer(user_save)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        data = request.DATA

        user_id = data.get('user_id')
        lab_proxy_id = data.get('lab_proxy_id')
        save_file = request.FILES['save_file']

        user = get_object_or_404(User, id=user_id)
        lab_proxy = get_object_or_404(LabProxy, id=lab_proxy_id)

        user_save = create_user_save(lab_proxy, user, save_file)

        serializer = UserSaveSerializer(user_save)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CreateErrorInfo(APIView):

    def get(self, request, *args, **kwargs):
        user_id = request.GET.get('user_id')
        lab_proxy_id = request.GET.get('lab_proxy_id')

        error_info = get_object_or_404(ErrorInfo, lab_proxy_id=lab_proxy_id, user_id=user_id)
        response = {
            'id': error_info.id,
            'user_lab_proxy_id': error_info.lab_proxy.id,
            'browser': error_info.browser,
            'os' : error_info.os,
            'user_agent' : error_info.user_agent,
            'message' : error_info.message,
            'date_encountered' : error_info.date_encountered,
        }
        return Response(response)

    def post(self, request, *args, **kwargs):
        data = request.DATA

        user_id = data.get('user_id')
        lab_proxy_id = data.get('lab_proxy_id')
        browser = data.get('browser')
        os = data.get('os')
        user_agent = data.get('user_agent')
        message = data.get('message')

        user = get_object_or_404(User, id=user_id)
        lab_proxy = get_object_or_404(LabProxy, id=lab_proxy_id)

        error_info, created = ErrorInfo.objects.get_or_create(
            user=user, lab_proxy=lab_proxy, browser=browser, os=os,
            user_agent=user_agent, message=message)        

        response = {
            'id': error_info.id,
            'user_lab_proxy_id': error_info.lab_proxy.id,
            'browser': error_info.browser,
            'os' : error_info.os,
            'user_agent' : error_info.user_agent,
            'message' : error_info.message,
            'date_encountered' : error_info.date_encountered,
        }

        http_status = status.HTTP_201_CREATED if created else status.HTTP_204_NO_CONTENT
        return Response(response, status=http_status)


class CreateDeviceInfo(APIView):

    def get(self, request, *args, **kwargs):
        user_id = request.GET.get('user_id')
        labProxy_id = request.GET.get('lab_proxy_id')

        device_info = get_object_or_404(DeviceInfo, labProxy_id=labProxy_id, user_id=user_id)
        response = {
            'id': device_info.id,
            'user_lab_proxy_id': device_info.labProxy.id,
            'device_id': device_info.device_id,
            'frame_rate': device_info.frame_rate,
            'os' : device_info.os,
            'type' : device_info.type,
            'ram' : device_info.ram,
            'processor' : device_info.processor,
            'cores' : device_info.cores,
            'gpu' : device_info.gpu,
            'memory' : device_info.memory,
            'fill_rate' : device_info.fill_rate,
            'shader_level' : device_info.shader_level,
            'quality' : device_info.quality,
            'misc' : device_info.misc,            
            'created_at' : device_info.created_at,
        }
        return Response(response)

    def post(self, request, *args, **kwargs):
        data = request.DATA

        user_id = data.get('user_id')
        lab_proxy_id = data.get('lab_proxy_id')
        device_id = data.get('device_id')
        os = data.get('os')
        frame_rate = data.get('frame_rate')
        type = data.get('type')
        ram = data.get('ram')
        processor = data.get('processor')
        cores = data.get('cores')
        gpu = data.get('gpu')
        memory = data.get('memory')
        fill_rate = data.get('fill_rate')
        shader_level = data.get('shader_level')
        quality = data.get('quality')
        misc = data.get('misc')

        user = get_object_or_404(User, id=user_id)
        labProxy = get_object_or_404(LabProxy, id=lab_proxy_id)

        device_info, created = DeviceInfo.objects.get_or_create(
            user=user, labProxy=labProxy, device_id=device_id,
            os=os, frame_rate=frame_rate, type=type, ram=ram,
            processor=processor, cores=cores, gpu=gpu, 
            memory=memory, fill_rate=fill_rate, misc=misc,
            shader_level=shader_level, quality=quality) 

        response = {
            'id': device_info.id,
            'user_lab_proxy_id': device_info.labProxy.id,
            'device_id': device_info.device_id,
            'frame_rate': device_info.frame_rate,
            'os' : device_info.os,
            'type' : device_info.type,
            'ram' : device_info.ram,
            'processor' : device_info.processor,
            'cores' : device_info.cores,
            'gpu' : device_info.gpu,
            'memory' : device_info.memory,
            'fill_rate' : device_info.fill_rate,
            'shader_level' : device_info.shader_level,
            'quality' : device_info.quality,
            'misc' : device_info.misc,            
            'created_at' : device_info.created_at,
        }

        http_status = status.HTTP_201_CREATED if created else status.HTTP_204_NO_CONTENT
        return Response(response, status=http_status)
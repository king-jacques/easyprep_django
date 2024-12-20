from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from tools.models import PromptLog
from tools.permissions import APIKeyAuthentication
from tools.serializers import EssaySerializer, GenericSerializer, PromptLogSerializer
from utils.open_ai.utils import send_prompt, run_prompts, custom_prompt, send_prompt_and_log
from rest_framework.exceptions import ParseError
import json
from django.http import HttpResponse
from rest_framework.settings import api_settings
from accounts.utils import log_activity #resource_type, resource_id, status, info
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from utils.open_ai.prompt_types import PROMPT_TYPES
from utils.open_ai.utils import MINI_MODEL, MAX_GPT_TOKENS
from drf_yasg.utils import swagger_auto_schema
# class HomePageView(TemplateView):
#     template_name = 'homepage.html'

from django.template import loader
from utils.open_ai.utils import get_default_prompt

def homepage_view(request):
    # template = loader.get_template('tools/homepage.html')  # Adjust the path as necessary
    template = loader.get_template('static/index.html')
    return HttpResponse(template.render())


class HomeView(viewsets.GenericViewSet):
    serializer_class = GenericSerializer
    parser_classes = [MultiPartParser, FormParser]
    
    @action(detail=False, methods=['GET',], permission_classes=[], )
    def heartbeat(self, request):
        # log_activity(request, action='pinging')
        return Response({"message": "Hello world!"})
        

class OpenAIView(viewsets.GenericViewSet):
    serializer_class = GenericSerializer
    @action(detail=False, methods=['POST',], permission_classes=[IsAuthenticated], )
    def send_prompt(self, request):
        prompt = request.data.get('prompt')
        model = request.data.get('model', MINI_MODEL)
        tokens = request.data.get('tokens', MAX_GPT_TOKENS)
        if not prompt:
            raise ParseError('Invalid Prompt')
        response = send_prompt(prompt, model)
        return Response({"response": response})
    
    @action(detail=False, methods=['POST',], permission_classes=[IsAuthenticated], )
    def download_prompt(self, request):
        as_json = request.data.get('as_json')
        use_default_prompt = request.data.get('use_default')
        
        model = request.data.get('model')
        tokens = request.data.get('tokens')
        items = request.data.get('items', [])
        
        data = None
        if use_default_prompt and not items:
            raise ParseError('Invalid items')
        
        if items and use_default_prompt:
            data, errors = run_prompts(items, use_default_prompt=use_default_prompt, use_timer=None)
            print(data)
            if as_json:
                json_data = json.dumps(data)
                response = HttpResponse(json_data, content_type='application/json')
                response['Content-Disposition'] = 'attachment; filename="data.json"'
                log_activity(request, action='prompt', info=request.data)
                return response

        tokens = request.data.get('tokens')
        prompt = request.data.get('prompt')

        if prompt:
            # data = send_prompt(prompt)
            log_activity(request, action='prompt')
            data = send_prompt_and_log(request, prompt, info=request.data)
            print("DATA!", data)

        return Response({"data": data})
        
    @action(detail=False, methods=['POST',], permission_classes=[IsAuthenticated], )
    def process_prompt(self, request):
        model = request.data.get('model')
        tokens = request.data.get('tokens')
        prompt = request.data.get('prompt')
        print(prompt)
        data, errors = run_prompts([prompt], use_default_prompt=False, use_timer=None)
        print(data, "DATA")
        print("ERRORS", errors)
        return Response({"data": data[0]})
    
    @action(detail=False, methods=['POST',], permission_classes=[IsAuthenticated], )
    def assessment_prompt(self, request):
        data = request.data
        content = data.get('content')
        if not content:
            return Response({'detail': "No 'content' provided" }, status=status.HTTP_400_BAD_REQUEST)
        exam_type = data.get('exam_type')
        if not exam_type:
            return Response({'detail': "No 'exam_type' provided" }, status=status.HTTP_400_BAD_REQUEST)
        instruction = data.get('instruction')
        if not instruction:
            return Response({'detail': "No 'instruction' provided" }, status=status.HTTP_400_BAD_REQUEST)
        exam_name = data.get('exam_name')
        callback_id = data.get('id')
        
    
        prompt_type = PROMPT_TYPES.get(exam_type)
        if not prompt_type:
            return Response({'detail': f"Invalid Exam Type: {exam_type}. accepted values are: {''.join(PROMPT_TYPES.keys())}"}, status=status.HTTP_400_BAD_REQUEST)

        prompt = prompt_type.format(essay = content, instruction = instruction)
        log_activity(request, action='prompt', info=request.data)
        response = send_prompt_and_log(request, prompt)
        # callback on callback_id???
        return Response({"data": response})
    
    @action(detail=False, methods=['GET',], permission_classes=[IsAuthenticated], )
    def my_prompts(self, request):
        user = request.user
        user_prompts = PromptLog.objects.filter(user=user)
        serializer = PromptLogSerializer(user_prompts, many=True)
        return Response(serializer.data)
    

from django.http import JsonResponse

class APIV1View(viewsets.GenericViewSet):
    authentication_classes = [APIKeyAuthentication] #+ api_settings.DEFAULT_AUTHENTICATION_CLASSES
    serializer_class = EssaySerializer

    @action(detail=False, methods=['GET',], permission_classes=[IsAuthenticated], )
    def prompt(self, request):
        user = request.user
        # If valid, continue with the request
        log_activity(request, action='prompt')
        return JsonResponse({'message': 'Success!', 'user': str(user)})

    @swagger_auto_schema(
        operation_summary="Review an Essay",
        operation_description="Review an Essay"
    )
    @action(detail=False, methods=['POST',], permission_classes=[IsAuthenticated], )
    def review_essay(self, request):
        data = request.data
        serializer = EssaySerializer(data=data)
        if serializer.is_valid():
            data = serializer.data
            prompt_type = PROMPT_TYPES.get(data['exam_type'])
            prompt = prompt_type.format(essay = data['content'], instruction = data['instruction'])
            response = send_prompt_and_log(request, prompt)
            log_activity(request, action='essay_review', type='Prompt')
            return Response(response)
        else:
            raise ParseError(serializer.errors)
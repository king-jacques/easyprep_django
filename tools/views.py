from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from utils.open_ai.utils import send_prompt, run_prompts
from rest_framework.exceptions import ParseError
import json
from django.http import HttpResponse

class HomeView(viewsets.GenericViewSet):
    parser_classes = [MultiPartParser, FormParser]

    @action(detail=False, methods=['GET',], permission_classes=[], )
    def heartbeat(self, request):
        return Response({"message": "Hello world!"})
        

class OpenAIView(viewsets.GenericViewSet):
    @action(detail=False, methods=['POST',], permission_classes=[], )
    def send_prompt(self, request):
        prompt = request.data.get('prompt')
        model = request.data.get('model')
        tokens = request.data.get('tokens')
        if not prompt:
            raise ParseError('Invalid Prompt')
        response = send_prompt(prompt, model, tokens)
        return Response({"response": response})
    
    @action(detail=False, methods=['POST',], permission_classes=[], )
    def download_prompt(self, request):
        use_default_prompt = request.data.get('use_default')
        prompts = request.data.get('prompts', [])
        if not prompts:
            raise ParseError('Invalid Prompt')
        data, errors = run_prompts(prompts, use_timer=0)
        json_data = json.dumps(data)
        response = HttpResponse(json_data, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="data.json"'
        return response
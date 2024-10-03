from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from tools.serializers import GenericSerializer
from utils.open_ai.utils import send_prompt, run_prompts
from rest_framework.exceptions import ParseError
import json
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views import View
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
# class HomePageView(TemplateView):
#     template_name = 'homepage.html'

from django.template import loader

def homepage_view(request):
    # template = loader.get_template('tools/homepage.html')  # Adjust the path as necessary
    template = loader.get_template('static/index.html')
    return HttpResponse(template.render())


class HomeView(viewsets.GenericViewSet):
    serializer_class = GenericSerializer
    parser_classes = [MultiPartParser, FormParser]
    
    @action(detail=False, methods=['GET',], permission_classes=[], )
    def heartbeat(self, request):
        return Response({"message": "Hello world!"})
        

class OpenAIView(viewsets.GenericViewSet):
    serializer_class = GenericSerializer
    @action(detail=False, methods=['POST',], permission_classes=[IsAuthenticated], )
    def send_prompt(self, request):
        prompt = request.data.get('prompt')
        model = request.data.get('model')
        tokens = request.data.get('tokens')
        if not prompt:
            raise ParseError('Invalid Prompt')
        response = send_prompt(prompt, model, tokens)
        return Response({"response": response})
    
    @action(detail=False, methods=['POST',], permission_classes=[IsAuthenticated], )
    def download_prompt(self, request):
        as_json = request.data.get('as_json')
        use_default_prompt = request.data.get('use_default')
        print("REQUEST DATA", request.data)
        model = request.data.get('model')
        tokens = request.data.get('tokens')
        items = request.data.get('items', [])
        print("ITEMS", items, use_default_prompt)
        data = None
        if use_default_prompt and not items:
            raise ParseError('Invalid items')
        
        if items and use_default_prompt:
            data, errors = run_prompts(items, use_default_prompt=use_default_prompt, use_timer=None)
            # data = json.loads(data)
            # print("ERRORS", errors)
            # print("TYPE", type(data))
            print(data)
            if as_json:
                json_data = json.dumps(data)
                response = HttpResponse(json_data, content_type='application/json')
                response['Content-Disposition'] = 'attachment; filename="data.json"'
                return response

        tokens = request.data.get('tokens')
        prompt = request.data.get('prompt')

        if prompt:
            data = send_prompt(prompt)
            print("DATA!", data)

        return Response({"data": data})
        
        
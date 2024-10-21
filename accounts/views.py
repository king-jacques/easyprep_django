from django.shortcuts import render
from django.contrib.auth import authenticate
from .serializers import SignUpSerializer, UserDetailSerializer
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.decorators import action
from .tokens import create_jwt_pair_for_user
from drf_yasg.utils import swagger_auto_schema
from django.template import loader
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now
from tools.utils import create_api_key_for_user
from tools.serializers import UserAPIKeySerializer
from .utils import log_activity, log_view_activity #resource_type, resource_id, status, info
# Create your views here.


class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = []

    @swagger_auto_schema(
        operation_summary="Create a user account",
        operation_description="This signs up a user"
    )
    def post(self, request: Request):
        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            user = serializer.save()
            log_activity(request, action='signup', user=user, type='User' )
            # response = {
            #     "message": "User Created Successfully",
            #     "data": serializer.data
            # }
            # return Response(data=response, status=status.HTTP_201_CREATED)
            tokens = create_jwt_pair_for_user(user)
            response = {
                "message": "Signup successful",
                "token": tokens,
                "user": {
                    "username": user.username,
                    "email": user.email,

                }
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        
        log_activity(request, action='signup', status='failed', info={
            'errors': str(serializer.errors)
        } )
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = []

    @swagger_auto_schema(
        operation_summary="Generate JWT pair",
        operation_description="This logs in a user with email and password"
    )
    def post(self, request: Request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)

        if user is not None:
            tokens = create_jwt_pair_for_user(user)
            response = {
                "message": "Login successful",
                "token": tokens,
                "user": {
                    "username": user.username,
                    "email": user.email,
                    
                }
            }
            user.last_login = now()
            user.save(update_fields=['last_login'])
            log_activity(request, action='login', user=user, type='User' )
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            log_activity(request=request, action='login', status='failed', info={
                'email': str(email),
                'password': str('password')
            })
            return Response(data={"message": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Get request info",
        operation_description="This shows the request information"
    )
    def get(self, request: Request):
        content = {
            "user": str(request.user),
            "auth": str(request.auth)
        }
        return Response(data=content, status=status.HTTP_200_OK)

class UserView(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserAPIKeySerializer
    @swagger_auto_schema(
        operation_summary="Get User Profile",
        operation_description="This returns User Data"
    )
    @action(detail=False, methods=['GET',])
    def profile(self, request:Request):
        user = request.user
        serializer = UserDetailSerializer(user)
        # log_activity(request, action='profile')
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create API Key",
        operation_description="This generates a new API Key for the user"
    )
    @action(detail=False, methods=['POST',])
    def create_api_key(self, request:Request):
        user = request.user
        key = create_api_key_for_user(user)
        data = UserAPIKeySerializer(key).data
        data['user'] = user.email
        log_activity(request, action='create_api_key', type='API' )
        return Response(data)


from django.template import loader

def homepage_view(request):
    template = loader.get_template('accounts/homepage.html')  # Adjust the path as necessary
    return HttpResponse(template.render())


def signup_view(request):
    if request.method == 'GET':
        template = loader.get_template('accounts/signup.html')
        return HttpResponse(template.render())
    elif request.method == 'POST':
        template = loader.get_template('accounts/signup.html')
        return HttpResponse(template.render())

def login_view(request):
    if request.method == 'GET':
        template = loader.get_template('accounts/login.html')
        return HttpResponse(template.render())
    elif request.method == 'POST':
        template = loader.get_template('accounts/login.html')
        return HttpResponse(template.render())
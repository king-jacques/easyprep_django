from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import APIKey

class ReadOnly(BasePermission):
    # overwrite the default has_permission
    def has_permission(self, request, view):
        # returns true for get and false for post
        return request.method in SAFE_METHODS


class AuthorOrReadOnly(BasePermission):
    # check if current user has object permission
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user == obj.author


class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.author


class AuthorOrPublic(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            if obj.public:
                return True
        return request.user == obj.author


class APIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        api_key_param = request.query_params.get('api_key')
        if auth_header and auth_header.startswith('Bearer '):
            try:
                auth_token = auth_header.split(' ')[1]
            except IndexError:
                raise AuthenticationFailed('Invalid token header. No token provided.')
        else:
            auth_token = None

        if not auth_token and api_key_param:
            auth_token = api_key_param

        if not auth_token:
            return None

        user = self.authenticate_api_key(auth_token)
        if not user:
            raise AuthenticationFailed('Invalid or inactive API key.')

        return (user, auth_token)
    
    def authenticate_api_key(self, api_key):
        try:
            api_key = APIKey.objects.get(key=api_key, is_active=True)
            api_key.increment_usage()
            return api_key.user  
        except APIKey.DoesNotExist:
            return None
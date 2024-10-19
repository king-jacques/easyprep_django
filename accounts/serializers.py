from rest_framework import serializers
from rest_framework.validators import ValidationError
from rest_framework import serializers
from .models import User, ActivityLog
from rest_framework.authtoken.models import Token
from tools.models import APIKey
from tools.serializers import UserAPIKeySerializer


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=80)
    username = serializers.CharField(max_length=45)
    # hide
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        email_exists = User.objects.filter(email=attrs['email']).exists()
        if email_exists:
            raise ValidationError("Email has already been used")
        return super().validate(attrs)

    # overwrite the create method with custom method to hide password chars in admin view
    def create(self, validated_data):
        password = validated_data.pop("password")

        user = super().create(validated_data)
        # actually update and hash password
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)
        return user


class CurrentUserNotesSerializer(serializers.ModelSerializer):
    # notes = serializers.StringRelatedField(many=True)
    notes = serializers.HyperlinkedRelatedField(
        many=True, view_name="note_detail", queryset=User.objects.all()
    )
    # url = serializers.HyperlinkedIdentityField(view_name="current_user")

    class Meta:
        model = User
        fields = ["id", "username", "email", "notes"]

class UserDetailSerializer(serializers.ModelSerializer):
    api_keys = serializers.SerializerMethodField()
    stats = serializers.SerializerMethodField()

    def get_stats(self, obj):
        if obj.is_staff or obj.is_superuser:
            return {
                'total_users': User.objects.count(),
                'recent_activity': ActivityLogSerializer(ActivityLog.objects.filter(action__in=('signup', 'create_api_key', 'essay_review')).exclude(status='failed').order_by('-timestamp')[:3], many=True).data
            }
        else:
            return {
                'total_users': 1,
                'recent_activity': ActivityLogSerializer(ActivityLog.objects.filter(user=obj, action__in=('signup', 'create_api_key', 'essay_review', 'prompt', 'login')).exclude(status='failed').order_by('-timestamp')[:3], many=True).data
            }
    def get_api_keys(self, obj):
        user_keys = APIKey.objects.filter(user = obj)[:3]
        return UserAPIKeySerializer(user_keys, many=True).data
    class Meta:
        model = User
        exclude = ('password', 'groups', 'user_permissions')

class ActivityLogSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()

    def get_title(self, obj):
        return ACTIVITY_TITLES.get(obj.action) or obj.action
    def get_user(self, obj):
        name = obj.user.username if obj.user else 'Anonymous'
        return  name or 'Anonymous'
    class Meta:
        model = ActivityLog
        fields = ('timestamp', 'user', 'type', 'title')


ACTIVITY_TITLES = {
    'signup': 'New User registered',
    'create_api_key': 'API Key Created',
    'prompt': 'Generated Prompt',
    'essay_review': 'Reviewed An Essay',
    'login': 'Logged In'
}
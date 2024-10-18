from rest_framework import serializers
from .models import PromptLog, APIKey
from utils.open_ai.prompt_types import PROMPT_TYPES
class GenericSerializer(serializers.Serializer):
    prompt = serializers.CharField()


class EssaySerializer(serializers.Serializer):
    instruction = serializers.CharField(required=True)
    exam_type = serializers.CharField(required=True)
    content = serializers.CharField()
    id = serializers.CharField(read_only=True)

    def validate_exam_type(self, value):
        if value not in PROMPT_TYPES.keys():
            raise serializers.ValidationError(f"Invalid value for 'exam_type'. Accepted values are: {''.join(PROMPT_TYPES.keys())}")
        return value
class PromptLogSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = PromptLog

class UserAPIKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = APIKey
        exclude = ('id', 'user', 'request_rate')
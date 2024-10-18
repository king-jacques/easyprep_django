from rest_framework import serializers
from .models import PromptLog
class GenericSerializer(serializers.Serializer):
    prompt = serializers.CharField()


class IELTSSerializer(serializers.Serializer):
    exam_name = serializers.CharField(max_length=100)
    exam_type = serializers.CharField(max_length=50)
    content = serializers.CharField()
    id = serializers.IntegerField(read_only=True)


class PromptLogSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = PromptLog
from rest_framework import serializers

class GenericSerializer(serializers.Serializer):
    prompt = serializers.CharField()
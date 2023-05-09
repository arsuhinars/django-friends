from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    name = serializers.CharField(required=True)


class UserCreateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

from enum import Enum

from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    name = serializers.CharField(required=True)


class UserCreateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class FriendshipStatus(str, Enum):
    NONE = 'NONE'
    INCOMING_INVITE = 'INCOMING_INVITE'
    OUTCOMING_INVITE = 'OUTCOMING_INVITE'
    FRIEND = 'FRIEND'

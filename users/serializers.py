from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User


class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate_username(self, username):
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise ValidationError('username is already taken')

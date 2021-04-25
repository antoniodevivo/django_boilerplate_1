from rest_framework import serializers
from bp_app.models import (Users)
from django.contrib.auth.models import update_last_login
from rest_framework_jwt.settings import api_settings

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

class UserLoginRegisterSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)

    def validate_username(self, username):
        if len(username) <= 3:
            raise serializers.ValidationError('Username is too short')
        import re
        if not re.match('^[a-z]+$', username):
            raise serializers.ValidationError('Username must only contains characters in lower case')
        return username
    
    def validate_password(self, password):
        if len(password) <= 3:
            raise serializers.ValidationError('Password is too short')
        return password

class UserTokenSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=255)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data["username"]
        user = Users.objects.filter(username=username).first()
        if user is None:
            raise serializers.ValidationError(
                'A user with this username and password is not found.'
            )
        payload = JWT_PAYLOAD_HANDLER(user)
        jwt_token = JWT_ENCODE_HANDLER(payload)
        update_last_login(None, user)
        return {
            'username':user.username,
            'token': jwt_token
        }
    
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        exclude = ["password"]
        read_only_fields = ['id']


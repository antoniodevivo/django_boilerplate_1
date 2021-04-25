from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from bp_app.models import Users
from bp_app.api.users.serializers import (UserSerializer, 
                                            UserTokenSerializer, 
                                            UserLoginRegisterSerializer
                                        )
from bp_app.api.permissions import IsAuthenticated
from bp_app.api.utils import CONST, get_csrf_token
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from django.contrib.auth import authenticate
import json


class LoginView(APIView):
    serializer_class = UserLoginRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            response = Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        else:
            username = request.data["username"]
            password = request.data["password"]
            user = authenticate(username=username, password=password)

            if user:
                serializer = UserTokenSerializer(data={"username": username})
                serializer.is_valid(raise_exception=True)
                expiration = (datetime.utcnow() + timedelta(hours=8))
                token = serializer.data["token"]
                response = Response(True, status.HTTP_200_OK)
                response.set_cookie(
                                        "auth_cookie",
                                        token,
                                        path='/',
                                        expires=expiration,
                                        httponly=True,
                                        
                                    )
            else:
                response = Response(False, status.HTTP_401_UNAUTHORIZED)
        return response

        
class CheckToken(APIView):
    def post(self, request):
        response = False
        token = get_csrf_token(request)
        serializer = VerifyJSONWebTokenSerializer(data={"token": token})
        if serializer.is_valid():
            response = True
        return Response(response, status.HTTP_200_OK)

class InfoUser(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = False
        token = CONST["token"]
        if token != None:
            serializer = UserSerializer(request.user, many=False)
            user = serializer.data
        return Response(user, status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        response = Response(True, status.HTTP_200_OK)
        response.set_cookie(
            'auth_cookie', max_age=0, path='/',
            expires='Thu, 01 Jan 1970 00:00:00 GMT',
        )
        return response


@api_view(["POST"])
@permission_classes([])
def register_api(request):
    user = Users(
        username=request.data.get("username"),
        password=request.data.get("password"),
        group_id=1
    )
    user.save()
    return Response(True)


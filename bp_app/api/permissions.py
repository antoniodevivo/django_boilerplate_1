from rest_framework import permissions
from bp_app.api.utils import CONST, get_csrf_token
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer

class IsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        token = get_csrf_token(request)
        serializer = VerifyJSONWebTokenSerializer(data={"token": token})
        if serializer.is_valid():
            CONST["token"] = token
            CONST["user"] = serializer.validated_data["user"]
            request.user = serializer.validated_data["user"]
            return True
        return False

class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        #can't work without IsAuthenticated first
        if request.user.group.rank_level > 1:
            return True
        return False

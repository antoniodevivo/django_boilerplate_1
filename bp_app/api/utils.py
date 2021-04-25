
CONST = {}

def get_csrf_token(request):
    return request._request.COOKIES.get("auth_cookie")

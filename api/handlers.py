from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    if isinstance(exc, InvalidToken):
        print({'success': False, 'message': '無效的token'})
    elif isinstance(exc, AuthenticationFailed):
        print({'success': False, 'message': '權限錯誤'})
    elif isinstance(exc, NotAuthenticated):
        print({'success': False, 'message': 'token遺失'})

    return Response({'success': False, 'message': '請重新登入'}, status=401)

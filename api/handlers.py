from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    if isinstance(exc, InvalidToken):
        return Response({'success': False, 'message': 'token錯誤'}, status=401)
    elif isinstance(exc, AuthenticationFailed):
        return Response({'success': False, 'message': '權限驗證錯誤'}, status=401)

    response = exception_handler(exc, context)

    return response

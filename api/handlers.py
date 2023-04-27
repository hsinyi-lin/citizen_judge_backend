from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    response_data = {'success': False}
    if isinstance(exc, InvalidToken):
        response_data['message'] = '無效的token'
    elif isinstance(exc, AuthenticationFailed):
        response_data['message'] = '權限錯誤'
    elif isinstance(exc, NotAuthenticated):
        response_data['message'] = 'token遺失'

    print(exc)

    if 'message' in response_data:
        return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)

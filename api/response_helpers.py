from rest_framework import status
from rest_framework.response import Response


def success_response(data=None, message='成功', status_code=status.HTTP_200_OK):
    response_data = {'success': True}
    if data is not None:
        response_data['data'] = data
    if message is not None:
        response_data['message'] = message
    return Response(response_data, status=status_code)


def error_response(message=None, status_code=status.HTTP_400_BAD_REQUEST):
    response_data = {'success': False}
    if message is not None:
        response_data['message'] = message
    return Response(response_data, status=status_code)


import hashlib
import random
import string
from email.mime.text import MIMEText

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from api.auth.serializers import *

from api.models import *

@api_view(['POST'])
def register(request):
    data = request.data

    if Account.objects.filter(email=data['email']).exists():
        return Response({
        'success': False,
        'message': '已註冊過此帳號'
    }, status=status.HTTP_409_CONFLICT)

    serializer = AccountSerializer(data=data)
    serializer.is_valid(raise_exception=True)

    sha256 = hashlib.sha256()
    sha256.update(serializer.validated_data['password'].encode('utf-8'))
    password_hash = sha256.hexdigest()
    serializer.validated_data['password'] = password_hash
    serializer.save()

    return Response({
        'success': True,
        'message': '註冊成功'
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    data = request.data

    sha256 = hashlib.sha256()
    sha256.update(data['password'].encode('utf-8'))
    password_hash = sha256.hexdigest()

    user = Account.objects.filter(email=data['email'], password=password_hash)
    if not user.exists():
        return Response({
            'success': False,
            'message': '帳號或密碼錯誤'
        }, status=status.HTTP_400_BAD_REQUEST)

    user = user.first()

    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    return Response({
        'success': True,
        'access_token': access_token,
    })


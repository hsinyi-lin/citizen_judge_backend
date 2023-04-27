import hashlib, random, string

from datetime import datetime

import jwt
from django.core.mail import send_mail
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from api.auth.serializers import *

from api.models import *
from api.response_helpers import *
from core import settings


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    data = request.data

    if Account.objects.filter(email=data['email']).exists():
        return error_response(message='已註冊過此帳號', status_code=status.HTTP_409_CONFLICT)

    serializer = AccountSerializer(data=data)
    serializer.is_valid(raise_exception=True)

    sha256 = hashlib.sha256()
    sha256.update(serializer.validated_data['password'].encode('utf-8'))
    password_hash = sha256.hexdigest()
    serializer.validated_data['password'] = password_hash
    serializer.save()

    return success_response(message='註冊成功', status_code=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    data = request.data

    sha256 = hashlib.sha256()
    sha256.update(data['password'].encode('utf-8'))
    password_hash = sha256.hexdigest()

    user = Account.objects.filter(email=data['email'], password=password_hash)
    if not user.exists():
        error_response(message='帳號或密碼錯誤')

    user = user.first()

    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    # decoded_token = jwt.decode(access_token, verify=False)
    # print(decoded_token)

    return Response({'success': True, 'access_token': access_token}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def send_code(request):
    data = request.data
    email = data.get('email')

    letters = string.ascii_letters + string.digits
    code = ''.join(random.choice(letters) for i in range(8))

    subject = 'Verification Code'
    message = f'您的驗證碼為: {code}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)

    VerificationCode.objects.create(email=email, code=code, create_time=datetime.now())

    return success_response(message='已發送驗證碼至您的信箱', status_code=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_code(request):
    data = request.data
    email = data.get('email')
    code = data.get('code')

    user_codes = VerificationCode.objects.filter(email=email).order_by('-id')
    if user_codes.exists() and user_codes.first().code == code:
        return success_response(message='驗證成功')

    return error_response(message='驗證碼錯誤', status_code=status.HTTP_404_NOT_FOUND)
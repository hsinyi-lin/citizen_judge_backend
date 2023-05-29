import hashlib, random, string

from django.core.mail import send_mail
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from api.auth.serializers import *

from api.models import *
from utils.response_helpers import *
from core import settings


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    data = request.data

    if Account.objects.filter(email=data['email'].strip()).exists():
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
    email = data.get('email').strip()
    password = data.get('password').strip()

    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    password_hash = sha256.hexdigest()

    user = Account.objects.filter(email=email, password=password_hash)
    if not user.exists():
        return error_response(message='帳號或密碼錯誤')

    user = user.first()

    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    # decoded_token = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
    # print(decoded_token)

    return Response({'success': True, 'message': '登入成功', 'access_token': access_token}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def send_code(request):
    data = request.data
    email = data.get('email').strip()
    is_forgot = bool(data['is_forgot_password'])

    account = Account.objects.filter(email=email)

    if is_forgot:
        if not account.exists():
            return error_response(message='此帳號未註冊過', status_code=status.HTTP_404_NOT_FOUND)
    else:
        if account.exists():
            return error_response(message='已註冊過此帳號', status_code=status.HTTP_409_CONFLICT)

    letters = string.ascii_letters + string.digits
    code = ''.join(random.choice(letters) for i in range(8))

    subject = 'Verification Code'
    message = f'您的驗證碼為: {code}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)

    VerificationCode.objects.create(email=email, code=code)

    return success_response(message='已發送驗證碼至您的信箱', status_code=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_code(request):
    data = request.data
    email = data.get('email').strip()
    code = data.get('code').strip()

    user_codes = VerificationCode.objects.filter(email=email).order_by('-id')
    if user_codes.exists() and user_codes.first().code == code:
        return success_response(message='驗證成功')

    return error_response(message='驗證碼錯誤', status_code=status.HTTP_404_NOT_FOUND)
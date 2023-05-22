import hashlib

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from api.models import *
from api.response_helpers import *


@api_view(['GET'])
@permission_classes([AllowAny])
def picture_list(request):
    pictures = Picture.objects.all()

    data = [
        {
            'id': picture.id,
            'picture': picture.photo
        }
        for picture in pictures
    ]

    return success_response(data=data)


@api_view(['GET'])
def get_account(request):
    data = request.data
    email = request.user_id

    acc = Account.objects.get(email=email)

    data = {
        'email': acc.email,
        'name': acc.name,
        'password': acc.password,
        'gender': acc.gender,
        'job_id': acc.job.id,
        'job_name': acc.job.name,
        'picture_id': acc.picture.id,
        'picture': acc.picture.photo,
        'is_notification': acc.is_notification,
        'is_quiz': acc.is_quiz
    }
    return success_response(data=data)


@api_view(['PATCH'])
def edit_account(request):
    data = request.data
    email = request.user_id
    name = data.get('name')
    gender = data.get('gender')
    job_id = data.get('job_id')
    picture_id = data.get('picture_id')

    acc = Account.objects.get(email=email)
    acc.name = name
    acc.gender = gender
    acc.job_id = job_id
    acc.picture_id = picture_id
    acc.save()

    return success_response(message='成功')


@api_view(['PATCH'])
@permission_classes([AllowAny])
def change_password(request):
    data = request.data
    email = data.get('email')

    acc = Account.objects.get(email=email)

    sha256 = hashlib.sha256()
    sha256.update(data['password'].encode('utf-8'))
    password_hash = sha256.hexdigest()
    acc.password = password_hash
    acc.save()

    return success_response(message='成功')


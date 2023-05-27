import hashlib

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from django.core.exceptions import ObjectDoesNotExist

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


@api_view(['POST'])
def add_quiz(request):
    data = request.data['data']
    email = request.user_id

    if len(data) != 5:
        return error_response(message='資料筆數不正確，應包含10筆資料', status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

    for item in data:
        question_id = item.get('question_id')
        score = item.get('score')
        Quiz.objects.create(question_id=question_id, email_id=email, score=score)

    try:
        acc = Account.objects.get(email=email)
    except Account.DoesNotExist:
        return error_response(message='帳號不存在', status_code=status.HTTP_404_NOT_FOUND)

    acc.is_quiz = 1
    acc.save()
    return success_response(message='成功')


@api_view(['GET'])
def collect_list(request):
    email = request.user_id

    try:
        saves = Saved.objects.filter(email_id=email)
        data_list = []
        for save in saves:
            try:
                like_count = Like.objects.filter(verdict=save.verdict).count()
                comment_count = Comment.objects.filter(verdict_id=save.verdict.id).count()
            except ObjectDoesNotExist:
                like_count = 0
                comment_count = 0

            data = {
                'verdict_id': save.verdict.id,
                'title': save.verdict.title,
                'judgement_date': save.verdict.judgement_date,
                'total_like': like_count,
                'total_comment': comment_count,
                'crime_id': save.verdict.crime.id,
                'crime_type': save.verdict.crime.name
            }
            data_list.append(data)

        return success_response(data=data_list)
    except ObjectDoesNotExist:
        return error_response(message='User not found', status_code=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def notice(request):
    data = request.data
    email = request.user_id
    is_notification = data.get('is_notification')

    if not data:
        return Response({'message': '缺少"is_notification"。'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        acc = Account.objects.get(email=email)
    except ObjectDoesNotExist:
        return Response({'message': '帳戶不存在。'}, status_code=status.HTTP_400_BAD_REQUEST)

    acc.is_notification = is_notification
    acc.save()
    return Response({'message': '成功'})

from django.db import IntegrityError
from django.db.models import Count
from rest_framework.decorators import api_view

from api.models import *
from api.verdict.serializers import VerdictSerializer, CustomVerdictSerializer
from utils.response_helpers import *


@api_view(['GET'])
def get_verdict(request):
    data = request.query_params
    email = request.user_id

    verdict_id = data.get('verdict_id')

    verdict = Verdict.objects.get(id=verdict_id)
    serializer = CustomVerdictSerializer(verdict, context={'email': email})
    serialized_data = serializer.data

    return success_response(data=serialized_data)


@api_view(['GET'])
def get_verdicts(request):
    data = request.query_params

    is_latest = int(data.get('is_latest'))
    page = int(data.get('page'))

    page_size = 30

    start_index = (page - 1) * page_size
    end_index = page * page_size

    if is_latest:
        verdicts = Verdict.objects.all().order_by('-judgement_date')[start_index:end_index]
    else:
        verdicts = Verdict.objects.annotate(like_count=Count('like')).order_by('-like_count')[start_index:end_index]

    serializer = VerdictSerializer(verdicts, many=True)
    serialized_data = serializer.data

    return success_response(data=serialized_data)


@api_view(['GET'])
def filter_verdicts(request):
    data = request.query_params

    title = data.get('title').strip()
    page = int(data.get('page'))

    page_size = 30

    start_index = (page - 1) * page_size
    end_index = page * page_size

    verdicts = Verdict.objects.filter(title__icontains=title).order_by('-judgement_date')[start_index:end_index]

    serializer = VerdictSerializer(verdicts, many=True)
    serialized_data = serializer.data

    return success_response(data=serialized_data)


@api_view(['GET'])
def get_crime_verdicts(request):
    data = request.query_params

    crime_id = data.get('crime_id')
    page = int(data.get('page'))

    page_size = 30

    start_index = (page - 1) * page_size
    end_index = page * page_size

    verdicts = Verdict.objects.filter(crime_id=crime_id).order_by('-judgement_date')[start_index:end_index]

    serializer = VerdictSerializer(verdicts, many=True)
    serialized_data = serializer.data

    return success_response(data=serialized_data)


@api_view(['POST'])
def like_verdict(request):
    data = request.data

    verdict_id = data.get('verdict_id')
    email = request.user_id

    try:
        Like.objects.create(verdict_id=verdict_id, email_id=email)
    except IntegrityError:
        return error_response(message='已按過讚', status_code=status.HTTP_409_CONFLICT)

    return success_response(message='成功', status_code=status.HTTP_201_CREATED)


@api_view(['DELETE'])
def unlike_verdict(request):
    data = request.data

    verdict_id = data.get('verdict_id')
    email = request.user_id

    like = Like.objects.filter(verdict_id=verdict_id, email_id=email)

    if not like.exists():
        return error_response(message='已收回讚', status_code=status.HTTP_410_GONE)

    like.delete()
    return success_response(message='成功')


@api_view(['POST'])
def collect_verdict(request):
    data = request.data

    verdict_id = data.get('verdict_id')
    email = request.user_id

    try:
        Saved.objects.create(verdict_id=verdict_id, email_id=email)
    except IntegrityError:
        return error_response(message='已收藏', status_code=status.HTTP_409_CONFLICT)

    return success_response(message='成功', status_code=status.HTTP_201_CREATED)


@api_view(['DELETE'])
def uncollect_verdict(request):
    data = request.data

    verdict_id = data.get('verdict_id')
    email = request.user_id

    saved = Saved.objects.filter(verdict_id=verdict_id, email_id=email)

    if not saved.exists():
        return error_response(message='已取消收藏', status_code=status.HTTP_410_GONE)

    saved.delete()
    return success_response(message='成功')

from django.db import IntegrityError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import *


@api_view(['GET'])
def get_verdict(request):
    data = request.query_params

    verdict_id = data.get('verdict_id')
    # user_id = request.user_id

    verdict = Verdict.objects.get(id=verdict_id)
    total_like = Like.objects.filter(verdict_id=verdict_id).count()
    total_comment = Comment.objects.filter(verdict_id=verdict_id).count()

    # recommendations
    # ....

    return Response({
        'success': True,
        'data': {
            'verdict_id': verdict.id,
            'title': verdict.title,
            'sub_title': verdict.sub_title,
            'ver_title': verdict.ver_title,
            'judgement_date': verdict.judgement_date,
            'incident': verdict.incident,
            'result': verdict.result,
            'laws': verdict.laws,
            'url': verdict.url,
            'crime_id': verdict.crime.id,
            'crime_type': verdict.crime.name,
            'total_like': total_like,
            'total_comment': total_comment,
            'create_time': verdict.create_time,
            'recommendations': []
        }
    })


@api_view(['GET'])

    return Response({
        'success': True,
        'data': [
            {
                'verdict_id': verdict.id,
                'title': verdict.title,
                'judgement_date': verdict.judgement_date,
                'total_like': Like.objects.filter(verdict_id=verdict.id).count(),
                'total_comment': Comment.objects.filter(verdict_id=verdict.id).count(),
                'crime_id': verdict.crime.id,
                'crime_type': verdict.crime.name
            }
            for verdict in verdicts
        ]
    })


@api_view(['GET'])
def filter_verdicts(request):
    data = request.query_params

    title = data.get('title').strip()
    # email = request.user_id

    verdicts = Verdict.objects.filter(title__icontains=title).order_by('-judgement_date')

    return Response({
        'success': True,
        'data': [
            {
                'verdict_id': verdict.id,
                'title': verdict.title,
                'judgement_date': verdict.judgement_date,
                'total_like': Like.objects.filter(verdict_id=verdict.id).count(),
                'total_comment': Comment.objects.filter(verdict_id=verdict.id).count(),
                'crime_id': verdict.crime.id,
                'crime_type': verdict.crime.name
            }
            for verdict in verdicts
        ]
    })


@api_view(['POST'])
def like_verdict(request):
    data = request.data

    verdict_id = data.get('verdict_id')
    email = request.user_id

    try:
        Like.objects.create(verdict_id=verdict_id, email_id=email)
    except IntegrityError:
        return Response({
            'success': False,
            'message': '已按讚過'
        }, status=status.HTTP_409_CONFLICT)

    return Response({
        'success': True,
        'message': '成功'
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def unlike_verdict(request):
    data = request.data

    verdict_id = data.get('verdict_id')
    email = request.user_id

    like = Like.objects.filter(verdict_id=verdict_id, email_id=email)

    if not like.exists():
        return Response({
            'success': False,
            'message': '已收回讚'
        }, status=status.HTTP_410_GONE)

    like.delete()

    return Response({
        'success': True,
        'message': '成功'
    }, status=status.HTTP_200_OK)



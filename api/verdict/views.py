from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import *


@api_view(['GET'])
def get_verdict_content(request):
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

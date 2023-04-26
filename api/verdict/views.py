from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import Verdict


@api_view(['GET'])
def get_verdict_content(request):
    data = request.query_params

    verdict_id = data.get('verdict_id')
    verdict = Verdict.objects.get(id=verdict_id)

    return Response({
        'success': True,
        'data': {
            'id': verdict.id,
            'title': verdict.title,
        }
    })

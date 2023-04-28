from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from api.models import Picture
from api.response_helpers import success_response


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
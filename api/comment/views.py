from django.db import IntegrityError
from rest_framework import status
from rest_framework.decorators import api_view

from api.models import *
from api.response_helpers import *


@api_view(['POST'])
def add_comment(request):
    data = request.data

    verdict_id = data.get('verdict_id')
    email = request.user_id
    content = data.get('content')

    if Comment.objects.filter(verdict_id=verdict_id,email=email).exists():
        return error_response(message='你已經留言過了')

    Comment.objects.create(verdict_id=verdict_id, email_id=email, content=content, is_edit=0)

    return success_response(message='成功', status_code=status.HTTP_201_CREATED)


@api_view(['DELETE'])
def delete_comment(request):
    data = request.data

    comment_id = data.get('comment_id')
    email = request.user_id

    comment = Comment.objects.filter(id=comment_id, email_id=email)

    if not comment.exists():
        return error_response(message='找無此留言', status_code=status.HTTP_410_GONE)

    comment.delete()
    return success_response(message='成功')


@api_view(['GET'])
def get_comments(request):
    data = request.query_params

    verdict_id = data.get('verdict_id')
    email = request.user_id

    comments = Comment.objects.filter(verdict_id=verdict_id)
    data = [
        {
            "comment_id": comment.id.id,
            "comment_email": comment.email.email,
            "job": comment.email.job.name,
            "comment": comment.content,
            "comment_create_time": comment.create_time,
            "replies": [
                # "reply_id":
                # "reply_email":
                # "job":
                # "reply":
                # "reply_create_time":
            ]
        }
        for comment in comments
    ]

    return success_response(data=data)


@api_view(['POST'])
def edit_comment(request):
    data = request.data

    verdict_id = data.get('verdict_id')
    email = request.user_id
    content = data.get('content')

    comment = Comment.objects.get(verdict_id=verdict_id, email_id=email)
    comment.content = content
    comment.is_edit = True
    comment.save()

    return success_response(message='成功')


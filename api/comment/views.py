from rest_framework.decorators import api_view


from django.core.exceptions import ObjectDoesNotExist
from api.models import *
from utils.response_helpers import *


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
    reply = Reply.objects.filter(comment_id=comment_id)

    if not comment.exists():
        return error_response(message='找無此留言', status_code=status.HTTP_410_GONE)
    
    reply.delete()
    comment.delete()

    return success_response(message='成功')


@api_view(['GET'])
def get_comments(request):
    data = request.query_params
    verdict_id = data.get('verdict_id')

    comments = Comment.objects.filter(verdict_id=verdict_id)
    data = []

    for comment in comments:
        replies = Reply.objects.filter(comment=comment)
        reply_data = [
            {
                "reply_id": reply.id,
                "reply_email": reply.email.pk,
                "job": reply.email.job.name,
                "reply": reply.content,
                "reply_create_time": reply.create_time,
                "reply_is_edited": reply.is_edit
            }
            for reply in replies
        ]

        comment_data = {
            "comment_id": comment.id.pk,
            "comment_email": comment.email.email,
            "job": comment.email.job.name,
            "comment": comment.content,
            "comment_create_time": comment.create_time,
            "replies": reply_data
        }

        data.append(comment_data)

    return success_response(data=data)


@api_view(['PATCH'])
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


@api_view(['POST'])
def add_reply(request):
    data = request.data

    comment_id = data.get('comment_id')
    email = request.user_id
    content = data.get('content')

    Reply.objects.create(comment_id=comment_id, email_id=email, content=content, is_edit=0)

    return success_response(message='成功', status_code=status.HTTP_201_CREATED)


@api_view(['DELETE'])
def delete_reply(request):
    data = request.data

    reply_id = data.get('reply_id')
    email = request.user_id

    reply = Reply.objects.filter(id=reply_id, email_id=email)

    if not reply.exists():
        return error_response(message='找無此回覆', status_code=status.HTTP_410_GONE)

    reply.delete()
    return success_response(message='成功')


@api_view(['PATCH'])
def edit_reply(request):
    data = request.data

    reply_id = data.get('reply_id')
    email = request.user_id
    content = data.get('content')

    try:
        reply = Reply.objects.get(id=reply_id, email_id=email)
    except ObjectDoesNotExist:
        return error_response(message='回覆不存在')

    reply.content = content
    reply.is_edit = True
    reply.save()

    return success_response(message='成功')


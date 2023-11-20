from rest_framework.decorators import api_view

from django.core.exceptions import ObjectDoesNotExist
from api.models import *
from utils.response_helpers import *
from collections import Counter, OrderedDict


@api_view(['POST'])
def add_comment(request):
    data = request.data
    crime_id = data.get('crime_id')
    verdict_id = data.get('verdict_id')
    email = request.user_id
    content = data.get('content')
    month = data.get('month')

    # 檢查是否已經留言過
    if Comment.objects.filter(verdict_id=verdict_id, email=email).exists():
        return Response({'message': '你已經留言過了'}, status=status.HTTP_400_BAD_REQUEST)

    # 創建 Comment 物件
    Comment.objects.create(verdict_id=verdict_id, email_id=email, content=content, is_edit=0)
    comment = Comment.objects.get(verdict_id=verdict_id, email_id=email)

    # 如果 crime_id 是1，則創建 CommentTheft 物件
    if crime_id == 1:
        is_money_related = data.get('is_money_related')
        is_abandoned = data.get('is_abandoned')
        is_indoor = data.get('is_indoor')
        is_destructive = data.get('is_destructive')
        is_group_crime = data.get('is_group_crime')
        is_transportation_used = data.get('is_transportation_used')
        has_criminal_record = data.get('has_criminal_record')
        is_income_tool = data.get('is_income_tool')
        CommentTheft.objects.create(comment=comment, is_money_related=is_money_related, is_abandoned=is_abandoned,
                                    is_indoor=is_indoor, is_destructive=is_destructive, is_group_crime=is_group_crime,
                                    is_transportation_used=is_transportation_used, has_criminal_record=has_criminal_record,
                                    is_income_tool=is_income_tool, month=month)
    elif crime_id == 2:
        is_attempted = data.get('is_attempted')
        is_child_victim = data.get('is_child_victim')
        is_family_relation = data.get('is_family_relation')
        is_mentally_ill = data.get('is_mentally_ill')
        is_money_dispute = data.get('is_money_dispute')
        is_prior_record = data.get('is_prior_record')
        is_emotional_dispute = data.get('is_emotional_dispute')
        is_intentional = data.get('is_intentional')
        CommentHomicide.objects.create(comment=comment, is_attempted=is_attempted, is_child_victim=is_child_victim,
                                    is_family_relation=is_family_relation, is_mentally_ill=is_mentally_ill, is_money_dispute=is_money_dispute,
                                    is_prior_record=is_prior_record,is_emotional_dispute=is_emotional_dispute,
                                    is_intentional=is_intentional, month=month)
    elif crime_id == 3:
        is_victim_injured = data.get('is_victim_injured')
        is_group_crime = data.get('is_group_crime')
        is_weapon_used = data.get('is_weapon_used')
        has_prior_record = data.get('has_prior_record')
        is_planned = data.get('is_planned')
        is_multi_victims = data.get('is_multi_victims')
        is_due_to_hardship = data.get('is_due_to_hardship')
        is_property_damaged = data.get('is_property_damaged')
        CommentRobbery.objects.create(comment=comment, is_victim_injured=is_victim_injured, is_group_crime=is_group_crime,
                                    is_weapon_used=is_weapon_used, has_prior_record=has_prior_record,
                                    is_planned=is_planned, is_multi_victims=is_multi_victims,
                                    is_due_to_hardship=is_due_to_hardship, is_property_damaged=is_property_damaged, month=month)
    elif crime_id == 4:
        has_driving_license = data.get('has_driving_license')
        has_passengers = data.get('has_passengers')
        affected_traffic_safety = data.get('affected_traffic_safety')
        caused_property_damage = data.get('caused_property_damage')
        is_professional_driver = data.get('is_professional_driver')
        hit_and_run = data.get('hit_and_run')
        victim_has_severe_injury = data.get('victim_has_severe_injury')
        weather_was_clear = data.get('weather_was_clear')
        CommentDriving.objects.create(comment=comment, has_driving_license=has_driving_license, has_passengers=has_passengers,
                                    affected_traffic_safety=affected_traffic_safety, caused_property_damage=caused_property_damage,
                                    is_professional_driver=is_professional_driver, hit_and_run=hit_and_run,
                                    victim_has_severe_injury=victim_has_severe_injury, weather_was_clear=weather_was_clear, month=month)
    else:
        return error_response(message='犯罪編號錯誤', status_code=status.HTTP_400_BAD_REQUEST)

    return success_response(message='成功', status_code=status.HTTP_201_CREATED)


@api_view(['DELETE'])
def delete_comment(request):
    data = request.data

    comment_id = data.get('comment_id')
    crime_id = data.get('crime_id')
    email = request.user_id

    comment = Comment.objects.filter(id=comment_id, email_id=email)
    reply = Reply.objects.filter(comment_id=comment_id)
    com_like = CommentLike.objects.filter(comment_id=comment_id)
    com_dislike = CommentDislike.objects.filter(comment_id=comment_id)
    if crime_id == 1:
        feature = CommentTheft.objects.filter(comment_id=comment_id)
    elif crime_id == 2:
        feature = CommentHomicide.objects.filter(comment_id=comment_id)
    elif crime_id == 3:
        feature = CommentRobbery.objects.filter(comment_id=comment_id)
    elif crime_id == 4:
        feature = CommentDriving.objects.filter(comment_id=comment_id)
    else:
        return error_response(message='犯罪編號錯誤', status_code=status.HTTP_400_BAD_REQUEST)

    if not comment.exists():
        return error_response(message='查無此留言', status_code=status.HTTP_410_GONE)

    reply.delete()
    feature.delete()
    com_like.delete()
    com_dislike.delete()
    comment.delete()
    
    return success_response(message='成功', status_code=status.HTTP_200_OK)


@api_view(['GET'])
def get_comments(request):
    data = request.query_params
    email = request.user_id
    verdict_id = data.get('verdict_id')
    crime_id = data.get('crime_id')

    comments = Comment.objects.filter(verdict_id=verdict_id)
    if not comments.exists():
        return error_response(message='查無此留言', status_code=status.HTTP_410_GONE)

    if not Comment.objects.filter(email=email, verdict_id=verdict_id).exists():
        return error_response(message='尚未留言', status_code=status.HTTP_410_GONE)

    data = []

    for comment in comments:
        replies = Reply.objects.filter(comment=comment)
        if crime_id == '1':
            theft = CommentTheft.objects.get(comment_id=comment)
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
                "is_edit": comment.is_edit,
                "comment_create_time": comment.create_time,
                "is_money_related": theft.is_money_related,
                "is_abandoned": theft.is_abandoned,
                "is_indoor": theft.is_indoor,
                "is_destructive": theft.is_destructive,
                "is_group_crime": theft.is_group_crime,
                "is_transportation_used": theft.is_transportation_used,
                "has_criminal_record": theft.has_criminal_record,
                "is_income_tool": theft.is_income_tool,
                "month": theft.month,
                "replies": reply_data
            }
        elif crime_id == '2':
            homicide = CommentHomicide.objects.get(comment_id=comment)
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
                "is_edit": comment.is_edit,
                "comment_create_time": comment.create_time,
                "is_attempted": homicide.is_attempted,
                "is_child_victim": homicide.is_child_victim,
                "is_family_relation": homicide.is_family_relation,
                "is_mentally_ill": homicide.is_mentally_ill,
                "is_money_dispute": homicide.is_money_dispute,
                "is_prior_record": homicide.is_prior_record,
                "is_emotional_dispute": homicide.is_emotional_dispute,
                "is_intentional": homicide.is_intentional,
                "month": homicide.month,
                "replies": reply_data
            }
        elif crime_id == '3':
            robbery = CommentRobbery.objects.get(comment_id=comment)
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
                "is_edit": comment.is_edit,
                "comment_create_time": comment.create_time,
                "is_victim_injured": robbery.is_victim_injured,
                "is_group_crime": robbery.is_group_crime,
                "is_weapon_used": robbery.is_weapon_used,
                "has_prior_record": robbery.has_prior_record,
                "is_planned": robbery.is_planned,
                "is_multi_victims": robbery.is_multi_victims,
                "is_due_to_hardship": robbery.is_due_to_hardship,
                "is_property_damaged": robbery.is_property_damaged,
                "month": robbery.month,
                "replies": reply_data
            }
        elif crime_id == '4':
            driving = CommentDriving.objects.get(comment_id=comment)
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
                "is_edit": comment.is_edit,
                "comment_create_time": comment.create_time,
                "has_driving_license": driving.has_driving_license,
                "has_passengers": driving.has_passengers,
                "affected_traffic_safety": driving.affected_traffic_safety,
                "caused_property_damage": driving.caused_property_damage,
                "is_professional_driver": driving.is_professional_driver,
                "hit_and_run": driving.hit_and_run,
                "victim_has_severe_injury": driving.victim_has_severe_injury,
                "weather_was_clear": driving.weather_was_clear,
                "month": driving.month,
                "replies": reply_data
            }
        else:
            return error_response(message='犯罪編號錯誤', status_code=status.HTTP_400_BAD_REQUEST)

        data.append(comment_data)

    return success_response(data=data)


@api_view(['PATCH'])
def edit_comment(request):
    data = request.data

    email = request.user_id
    comment_id = data.get('comment_id')
    content = data.get('content')
    month = data.get('month')
    crime_id = data.get('crime_id')

    try:
        comment = Comment.objects.get(id=comment_id, email=email)

        comment.content = content
        comment.is_edit = True
        comment.save()

        if crime_id == 1:
            theft = CommentTheft.objects.get(comment_id=comment_id)
            is_money_related = data.get('is_money_related')
            is_abandoned = data.get('is_abandoned')
            is_indoor = data.get('is_indoor')
            is_destructive = data.get('is_destructive')
            is_group_crime = data.get('is_group_crime')
            is_transportation_used = data.get('is_transportation_used')
            has_criminal_record = data.get('has_criminal_record')
            is_income_tool = data.get('is_income_tool')
            theft.is_money_related = is_money_related
            theft.is_abandoned = is_abandoned
            theft.is_indoor = is_indoor
            theft.is_destructive = is_destructive
            theft.is_group_crime = is_group_crime
            theft.is_transportation_used = is_transportation_used
            theft.has_criminal_record = has_criminal_record
            theft.is_income_tool = is_income_tool
            theft.month = month
            theft.save()
        elif crime_id == 2:
            is_attempted = data.get('is_attempted')
            is_child_victim = data.get('is_child_victim')
            is_family_relation = data.get('is_family_relation')
            is_mentally_ill = data.get('is_mentally_ill')
            is_money_dispute = data.get('is_money_dispute')
            is_prior_record = data.get('is_prior_record')
            is_emotional_dispute = data.get('is_emotional_dispute')
            is_intentional = data.get('is_intentional')
            homicide = CommentHomicide.objects.get(comment_id=comment_id)
            homicide.is_attempted = is_attempted
            homicide.is_child_victim = is_child_victim
            homicide.is_family_relation = is_family_relation
            homicide.is_mentally_ill = is_mentally_ill
            homicide.is_group_crime = is_money_dispute
            homicide.is_prior_record = is_prior_record
            homicide.is_emotional_dispute = is_emotional_dispute
            homicide.is_intentional = is_intentional
            homicide.month = month
            homicide.save()
        elif crime_id == 3:
            is_victim_injured = data.get('is_victim_injured')
            is_group_crime = data.get('is_group_crime')
            is_weapon_used = data.get('is_weapon_used')
            has_prior_record = data.get('has_prior_record')
            is_planned = data.get('is_planned')
            is_multi_victims = data.get('is_multi_victims')
            is_due_to_hardship = data.get('is_due_to_hardship')
            is_property_damaged = data.get('is_property_damaged')
            robbery = CommentRobbery.objects.get(comment_id=comment_id)
            robbery.is_victim_injured = is_victim_injured
            robbery.is_group_crime = is_group_crime
            robbery.is_weapon_used = is_weapon_used
            robbery.has_prior_record = has_prior_record
            robbery.is_planned = is_planned
            robbery.is_multi_victims = is_multi_victims
            robbery.is_due_to_hardship = is_due_to_hardship
            robbery.is_property_damaged = is_property_damaged
            robbery.month = month
            robbery.save()
        elif crime_id == 4:
            has_driving_license = data.get('has_driving_license')
            has_passengers = data.get('has_passengers')
            affected_traffic_safety = data.get('affected_traffic_safety')
            caused_property_damage = data.get('caused_property_damage')
            is_professional_driver = data.get('is_professional_driver')
            hit_and_run = data.get('hit_and_run')
            victim_has_severe_injury = data.get('victim_has_severe_injury')
            weather_was_clear = data.get('weather_was_clear')
            driving = CommentDriving.objects.get(comment_id=comment_id)
            driving.has_driving_license = has_driving_license
            driving.has_passengers = has_passengers
            driving.affected_traffic_safety = affected_traffic_safety
            driving.caused_property_damage = caused_property_damage
            driving.is_professional_driver = is_professional_driver
            driving.hit_and_run = hit_and_run
            driving.victim_has_severe_injury = victim_has_severe_injury
            driving.weather_was_clear = weather_was_clear
            driving.month = month
            driving.save()

    except Comment.DoesNotExist:
        return error_response(message='查無此留言', status_code=status.HTTP_410_GONE)

    return success_response(message='成功')


@api_view(['POST'])
def add_reply(request):
    data = request.data

    comment_id = data.get('comment_id')
    email = request.user_id
    content = data.get('content')

    if content == "":
        return error_response(message='請輸入文字再回覆', status_code=status.HTTP_400_BAD_REQUEST)

    try:
        Reply.objects.create(comment_id=comment_id, email_id=email, content=content, is_edit=0)
    except:
        return error_response(message='找無此留言所以無法回覆', status_code=status.HTTP_404_NOT_FOUND)

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


@api_view(['POST'])
def add_like(request):
    data = request.data
    comment_id = data.get('comment_id')
    email = request.user_id

    # 確認是否有提供comment_id
    if not comment_id:
        return error_response(message='沒有回傳comment_id', status_code=status.HTTP_400_BAD_REQUEST)

    # 檢查comment_id是否存在於Comment資料表中
    if not Comment.objects.filter(id=comment_id).exists():
        return error_response(message='找不到指定的評論', status_code=status.HTTP_404_NOT_FOUND)

    # 嘗試創建一個新的CommentLike記錄
    try:
        comment_like, created = CommentLike.objects.get_or_create(comment_id=comment_id, email_id=email)
        if created:
            return success_response(message='成功')
        else:
            return error_response(message='CommentLike對象已存在', status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        return error_response(message=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def add_dislike(request):
    data = request.data
    comment_id = data.get('comment_id')
    email = request.user_id

    # 確認是否有提供comment_id
    if not comment_id:
        return error_response(message='沒有回傳comment_id', status_code=status.HTTP_400_BAD_REQUEST)

    # 檢查comment_id是否存在於Comment資料表中
    if not Comment.objects.filter(id=comment_id).exists():
        return error_response(message='找不到指定的評論', status_code=status.HTTP_404_NOT_FOUND)

    # 嘗試創建一個新的CommentLike記錄
    try:
        comment_dislike, created = CommentDislike.objects.get_or_create(comment_id=comment_id, email_id=email)
        if created:
            return success_response(message='成功')
        else:
            return error_response(message='CommentLike對象已存在', status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        return error_response(message=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def delete_like(request):
    data = request.data
    comment_id = data.get('comment_id')
    email = request.user_id

    if not comment_id:
        return error_response(message='沒有回傳comment_id', status_code=status.HTTP_400_BAD_REQUEST)

    comment_like = CommentLike.objects.filter(comment_id=comment_id, email_id=email)
    if not comment_like:
        return error_response(message='找不到該筆資料', status_code=status.HTTP_404_NOT_FOUND)

    comment_like.delete()
    return success_response(message='成功')


@api_view(['DELETE'])
def delete_dislike(request):
    data = request.data
    comment_id = data.get('comment_id')
    email = request.user_id

    if not comment_id:
        return error_response(message='沒有回傳comment_id', status_code=status.HTTP_400_BAD_REQUEST)

    comment_dislike = CommentDislike.objects.filter(comment_id=comment_id, email_id=email)
    if not comment_dislike:
        return error_response(message='找不到該筆資料', status_code=status.HTTP_404_NOT_FOUND)

    comment_dislike.delete()
    return success_response(message='成功')


@api_view(['GET'])
def likes(request):
    data = request.query_params
    comment_id = data.get('comment_id')

    total = CommentLike.objects.filter(comment_id=comment_id).count()
    return success_response(total)


@api_view(['GET'])
def dislikes(request):
    data = request.query_params
    comment_id = data.get('comment_id')

    total = CommentDislike.objects.filter(comment_id=comment_id).count()
    return success_response(total)


@api_view(['POST'])
def feature(request):
    data = request.data
    verdict_id = data.get('verdict_id')
    crime_id = data.get('crime_id')

    comments = Comment.objects.filter(verdict_id=verdict_id)
    num_comments = comments.count()

    if num_comments <= 5:
        return error_response(message='資料不足', status_code=status.HTTP_400_BAD_REQUEST)

    if crime_id == 1:  # theft
        count_is_money_related = 0
        count_is_abandoned = 0
        count_is_indoor = 0
        count_is_destructive = 0
        count_is_group_crime = 0
        count_is_transportation_used = 0
        count_has_criminal_record = 0
        count_is_income_tool = 0

        for comment in comments:
            theft = CommentTheft.objects.get(comment=comment)
            if theft.is_money_related:
                count_is_money_related += 1
            if theft.is_abandoned:
                count_is_abandoned += 1
            if theft.is_indoor:
                count_is_indoor += 1
            if theft.is_destructive:
                count_is_destructive += 1
            if theft.is_group_crime:
                count_is_group_crime += 1
            if theft.is_transportation_used:
                count_is_transportation_used += 1
            if theft.has_criminal_record:
                count_has_criminal_record += 1
            if theft.is_income_tool:
                count_is_income_tool += 1

        stats_data = {
            "is_money_related": count_is_money_related,
            "is_abandoned": count_is_abandoned,
            "is_indoor": count_is_indoor,
            "is_destructive": count_is_destructive,
            "is_group_crime": count_is_group_crime,
            "is_transportation_used": count_is_transportation_used,
            "has_criminal_record": count_has_criminal_record,
            "is_income_tool": count_is_income_tool,
        }

    elif crime_id == 2:  # homicide
        count_is_attempted = 0
        count_is_family_relation = 0
        count_is_child_victim = 0
        count_is_mentally_ill = 0
        count_is_money_dispute = 0
        count_is_prior_record = 0
        count_is_emotional_dispute = 0
        count_is_intentional = 0

        for comment in comments:
            homicide = CommentHomicide.objects.get(comment=comment)
            if homicide.is_attempted:
                count_is_attempted += 1
            if homicide.is_family_relation:
                count_is_family_relation += 1
            if homicide.is_child_victim:
                count_is_child_victim += 1
            if homicide.is_mentally_ill:
                count_is_mentally_ill += 1
            if homicide.is_money_dispute:
                count_is_money_dispute += 1
            if homicide.is_prior_record:
                count_is_prior_record += 1
            if homicide.is_emotional_dispute:
                count_is_emotional_dispute += 1
            if homicide.is_intentional:
                count_is_intentional += 1

        stats_data = {
            "is_attempted": count_is_attempted,
            "is_family_relation": count_is_family_relation,
            "is_child_victim": count_is_child_victim,
            "is_mentally_ill": count_is_mentally_ill,
            "is_money_dispute": count_is_money_dispute,
            "is_prior_record": count_is_prior_record,
            "is_emotional_dispute": count_is_emotional_dispute,
            "is_intentional": count_is_intentional,
        }

    elif crime_id == 3:  # robbery
        count_is_victim_injured = 0
        count_is_group_crime = 0
        count_is_weapon_used = 0
        count_has_prior_record = 0
        count_is_planned = 0
        count_is_multi_victims = 0
        count_is_due_to_hardship = 0
        count_is_property_damaged = 0

        for comment in comments:
            robbery = CommentRobbery.objects.get(comment=comment)
            if robbery.is_victim_injured:
                count_is_victim_injured += 1
            if robbery.is_group_crime:
                count_is_group_crime += 1
            if robbery.is_weapon_used:
                count_is_weapon_used += 1
            if robbery.has_prior_record:
                count_has_prior_record += 1
            if robbery.is_planned:
                count_is_planned += 1
            if robbery.is_multi_victims:
                count_is_multi_victims += 1
            if robbery.is_due_to_hardship:
                count_is_due_to_hardship += 1
            if robbery.is_property_damaged:
                count_is_property_damaged += 1

        stats_data = {
            "is_victim_injured": count_is_victim_injured,
            "is_group_crime": count_is_group_crime,
            "is_weapon_used": count_is_weapon_used,
            "has_prior_record": count_has_prior_record,
            "is_planned": count_is_planned,
            "is_multi_victims": count_is_multi_victims,
            "is_due_to_hardship": count_is_due_to_hardship,
            "is_property_damaged": count_is_property_damaged,
        }

    elif crime_id == 4:  # driving
        count_has_driving_license = 0
        count_has_passengers = 0
        count_affected_traffic_safety = 0
        count_caused_property_damage = 0
        count_is_professional_driver = 0
        count_hit_and_run = 0
        count_victim_has_severe_injury = 0
        count_weather_was_clear = 0

        for comment in comments:
            driving = CommentDriving.objects.get(comment=comment)
            if driving.has_driving_license:
                count_has_driving_license += 1
            if driving.has_passengers:
                count_has_passengers += 1
            if driving.affected_traffic_safety:
                count_affected_traffic_safety += 1
            if driving.caused_property_damage:
                count_caused_property_damage += 1
            if driving.is_professional_driver:
                count_is_professional_driver += 1
            if driving.hit_and_run:
                count_hit_and_run += 1
            if driving.victim_has_severe_injury:
                count_victim_has_severe_injury += 1
            if driving.weather_was_clear:
                count_weather_was_clear += 1

        stats_data = {
            "has_driving_license": count_has_driving_license,
            "has_passengers": count_has_passengers,
            "affected_traffic_safety": count_affected_traffic_safety,
            "caused_property_damage": count_caused_property_damage,
            "is_professional_driver": count_is_professional_driver,
            "hit_and_run": count_hit_and_run,
            "victim_has_severe_injury": count_victim_has_severe_injury,
            "weather_was_clear": count_weather_was_clear,
        }

    return success_response(data=stats_data)


@api_view(['POST'])
def month(request):
    data = request.data
    verdict_id = data.get('verdict_id')
    crime_id = data.get('crime_id')

    comments = Comment.objects.filter(verdict_id=verdict_id)
    num_comments = comments.count()

    # 計算comments的資料筆數
    if num_comments <= 5:
        # 筆數不足 5 筆，回傳失敗訊息
        return error_response(message='資料不足', status_code=status.HTTP_400_BAD_REQUEST)

    month_data = []

    for comment in comments:
        if crime_id == 1:  # theft
            theft = CommentTheft.objects.get(comment_id=comment)
            month_data.append(theft.month)  # 假設 CommentTheft 物件有 month 屬性

        elif crime_id == 2:  # homicide
            homicide = CommentHomicide.objects.get(comment_id=comment)
            month_data.append(homicide.month)

        elif crime_id == 3:  # robbery
            robbery = CommentRobbery.objects.get(comment_id=comment)
            month_data.append(robbery.month)

        elif crime_id == 4:  # driving
            driving_incident = CommentDriving.objects.get(comment_id=comment)
            month_data.append(driving_incident.month)

        # TODO: 如果還有其他犯罪類型，可以在這裡繼續加

    # 使用 Counter 計算每個月份出現的次數
    month_counter = Counter(month_data)

    # 將字典按照鍵值排序
    sorted_month_counter = OrderedDict(sorted(month_counter.items()))

    return success_response(data=sorted_month_counter)

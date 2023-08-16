import numpy as np
from rest_framework import serializers

from api.models import *
from django.db.models import Q

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


class VerdictSerializer(serializers.ModelSerializer):
    verdict_id = serializers.IntegerField(source='id')
    total_like = serializers.SerializerMethodField()
    total_comment = serializers.SerializerMethodField()
    crime_id = serializers.IntegerField(source='crime.id')
    crime_type = serializers.CharField(source='crime.name', read_only=True)

    class Meta:
        model = Verdict
        fields = ['verdict_id', 'title', 'judgement_date', 'total_like', 'total_comment', 'crime_id', 'crime_type']

    def get_total_like(self, obj):
        return Like.objects.filter(verdict_id=obj.id).count()

    def get_total_comment(self, obj):
        return Comment.objects.filter(verdict_id=obj.id).count()


class CustomVerdictSerializer(VerdictSerializer):
    incident = serializers.SerializerMethodField()
    result = serializers.SerializerMethodField()
    laws = serializers.SerializerMethodField()
    recommendations = serializers.SerializerMethodField()

    class Meta(VerdictSerializer.Meta):
        fields = VerdictSerializer.Meta.fields + ['sub_title', 'ver_title', 'incident', 'incident_lite',
                                                  'result', 'url', 'create_time', 'laws', 'recommendations']

    def get_incident(self, obj):
        return obj.incident.split('\n')

    def get_result(self, obj):
        return obj.result.split('\n')

    def get_laws(self, obj):
        if obj.laws is None:
            return obj.laws
        return obj.laws.split(',')

    def get_recommendations(self, obj):
        email = self.context.get('email')
        verdict_id = obj.id

        # --- 排除已留言過的判決書(之後再判斷其他犯罪類型) ---
        verdict_ids = Comment.objects.filter(email=email).values_list('verdict_id', flat=True)

        # 使填寫過留言的判例不可推薦，但還是可以從搜尋點入該判例
        if verdict_id in verdict_ids:
            verdict_ids = [id for id in verdict_ids if id != verdict_id]


        data, feature_columns = None, None

        if obj.crime_id == 1:
            # 排除已留言過的文章
            data = TheftFeature.objects.exclude(id__in=verdict_ids)
            # 取得特徵列名稱
            feature_columns = [field.name for field in TheftFeature._meta.get_fields()][1:-1]
        elif obj.crime_id == 2:
            return []
        elif obj.crime_id == 3:
            data = RobberyFeature.objects.exclude(id__in=verdict_ids)
            feature_columns = [field.name for field in RobberyFeature._meta.get_fields()][1:-3]
        else:
            return []

        # QuerySet 轉換成 Pandas DataFrame、計算特徵之間的相似度矩陣
        data_df = pd.DataFrame.from_records(data.values_list(*feature_columns))
        similarity_matrix = cosine_similarity(data_df)

        # 該判決書 verdict_id 在 QuerySet 的位置

        index = list(data.values_list('id', flat=True)).index(verdict_id)
        # print(index)
        # print(data[index])

        # 取得相似度(遞減)的判決書索引
        similar_verdicts_indices = similarity_matrix[index].argsort()[::-1]
        # print(similar_verdicts_indices)

        # 移除 verdict_id 在 QuerySet 的位置的值
        indices_to_remove = np.where(similar_verdicts_indices == index)[0]
        # print(indices_to_remove)
        similar_articles_indices = np.delete(similar_verdicts_indices, indices_to_remove)
        # print(similar_articles_indices)

        # 取得 data 的索引列表以獲取對應索引的 data 資料
        data_indices = similar_articles_indices[:3]
        recommendation_ids = [data[index].pk for index in data_indices.tolist()]
        # print(recommendation_ids)

        # 獲取字典形式的判決書，確保按照推薦順序進行推薦
        verdicts_dict = Verdict.objects.in_bulk(recommendation_ids)
        verdicts = [verdicts_dict[id] for id in recommendation_ids]

        serializer = VerdictSerializer(verdicts, many=True)

        return serializer.data

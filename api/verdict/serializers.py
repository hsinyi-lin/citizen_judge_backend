from rest_framework import serializers

from api.models import *


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
        return obj.laws.split(',')

    def get_recommendations(self, obj):
        recommendation_verdicts = Verdict.objects.filter(id__in=[1,3])
        serializer = VerdictSerializer(recommendation_verdicts, many=True)
        return serializer.data
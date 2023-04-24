from rest_framework import serializers
from api.models import *

class AccountSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    job_id = serializers.PrimaryKeyRelatedField(queryset=Job.objects.all(), source='job')
    picture_id = serializers.PrimaryKeyRelatedField(queryset=Picture.objects.all(), source='picture')

    class Meta:
        model = Account
        fields = ['email', 'name', 'password', 'gender', 'birth', 'job_id', 'picture_id', 'is_notification']

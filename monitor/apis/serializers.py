from rest_framework import serializers
from .models import Historicallogs
from core.models import Website

class LogsSerializer(serializers.HyperlinkedModelSerializer):
    websites = serializers.HyperlinkedIdentityField(view_name="core:user-detail")


    class Meta:
        model = Historicallogs
        fields = ('websites', 'is_url_valid', 'user', 'is_active', 'timestamp')

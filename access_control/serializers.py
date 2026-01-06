from rest_framework import serializers
from .models import AccessLog

class AccessLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = AccessLog
        fields = ['id', 'card_id', 'door_name', 'access_granted', 'timestamp']
        read_only_fields = ['timestamp']
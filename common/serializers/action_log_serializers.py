from rest_framework import serializers

from common.models.action_log import ActionLog

class ActionLogSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = ActionLog
        fields = ['id', 'user', 'action', 'timestamp', 'details']
        read_only_fields = fields
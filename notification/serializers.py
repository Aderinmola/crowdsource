from rest_framework import serializers
from .models import Notification
from django.contrib.contenttypes.models import ContentType

class NotificationSerializer(serializers.ModelSerializer):
    actor_username = serializers.CharField(source='actor.username', read_only=True)
    target_type = serializers.SerializerMethodField()
    target_id = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            'id', 'recipient', 'actor', 'actor_username', 'verb',
            'target_type', 'target_id', 'is_read', 'timestamp'
        ]

    def get_target_type(self, obj):
        return obj.content_type.model

    def get_target_id(self, obj):
        return obj.object_id

from django.contrib.contenttypes.models import ContentType
from .models import Notification

def create_notification(actor, recipient, verb, target):
    content_type = ContentType.objects.get_for_model(target.__class__)
    Notification.objects.create(
        actor=actor,
        recipient=recipient,
        verb=verb,
        content_type=content_type,
        object_id=target.id
    )

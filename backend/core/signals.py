from django.db.models.signals import post_delete
from django.dispatch import receiver

from recipes.models import Recipe


@receiver(post_delete, sender=Recipe)
def delete_image(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(False)

import os
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import Recipe

@receiver(post_delete, sender=Recipe)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Borra el archivo del sistema cuando se elimina el objeto de la base de datos.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

@receiver(pre_save, sender=Recipe)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Borra el archivo antiguo cuando se sube uno nuevo.
    """
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).image
    except sender.DoesNotExist:
        return False

    new_file = instance.image
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
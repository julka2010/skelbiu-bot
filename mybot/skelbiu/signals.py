import os
from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import AdvertisementImage

def _delete_file(path):
   """ Deletes file from filesystem.

       Copy-pasted from sobolenv's SO answer
       https://stackoverflow.com/a/33081018/4371768
   """
   if os.path.isfile(path):
       os.remove(path)

@receiver(post_delete, sender=AdvertisementImage)
def delete_file(sender, instance, *args, **kwargs):
    """ Deletes image files on `post_delete`

       Copy-pasted from sobolenv's SO answer
       https://stackoverflow.com/a/33081018/4371768
    """
    if instance.image:
        _delete_file(instance.image.path)

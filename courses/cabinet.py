from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from cabinet.base import AbstractFile, ImageMixin, DownloadMixin





    # Add additional fields if you want to.

# If files should be automatically deleted (this is also the case when
# using the default file model):
@receiver(signals.post_delete, sender=File)
def delete_files(sender, instance, **kwargs):
    instance.delete_files()
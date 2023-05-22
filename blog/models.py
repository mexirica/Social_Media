import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from stdimage import StdImageField, JPEGField

class CustomUser(AbstractUser):
    profile_picture = models.ImageField(_('profile picture'), upload_to='profile_pictures', null=True, blank=True)


class Photo(models.Model):
    title = models.CharField(max_length=50)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    subtitle = models.CharField(max_length=100)
    photo = StdImageField(upload_to='profile_pictures', variations={'thumbnail': {"width": 270, "height": 180, "crop": True}})
    created_at= models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Photo"
        verbose_name_plural = "Photos"
        permissions = [
            ('can_edit_photo', 'Can edit photo'),
            ('can_delete_photo', 'Can delete photo')
        ]
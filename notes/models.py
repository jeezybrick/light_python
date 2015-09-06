import datetime
import os
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.core.files.storage import FileSystemStorage


# Класс для перезаписи существующих файлов
class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


class MyUser(AbstractUser):
    date_of_birth = models.DateField(default=datetime.datetime.now)
    phone = models.CharField(_('Телефон'), max_length=40, default='', blank=False, null=False)
    avatar = models.ImageField(upload_to='notes/avatars/', blank=True, storage=OverwriteStorage())
    is_private = models.BooleanField(_('Приватные заметки'), default=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    class Meta(object):
        unique_together = ('email',)


class ColorOfNote(models.Model):
    name = models.CharField(_("Цвет заметки"), max_length=30, blank=True)
    color = models.CharField(_("Цвет в hex"), max_length=30, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)
    parent_category = models.ForeignKey("self", blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.name


class LabelDefault(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Notes(models.Model):
    title = models.CharField(_('Название'), max_length=50, blank=False)
    message = models.CharField(_("Текст"), max_length=1000, blank=False)
    file = models.FileField(upload_to='notes/files/', blank=True)
    color = models.ForeignKey(ColorOfNote, blank=True, default='1', null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    categories = models.ManyToManyField(Category, blank=True)
    labels = models.ManyToManyField(LabelDefault, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.message


class LabelCustom(models.Model):
    file = models.ImageField(upload_to='notes/labels/custom/', blank=True)
    note = models.ForeignKey(Notes, blank=True, null=True)

    def __str__(self):
        return str(self.file)
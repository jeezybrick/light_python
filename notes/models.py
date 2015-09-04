from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
# Create your models here.


class ColorOfNote(models.Model):
    color = models.CharField(_("Цвет заметки"), max_length=30, blank=True)

    def __str__(self):
        return self.color


class Notes(models.Model):
    title = models.CharField(_('Название'), max_length=100, blank=False)
    message = models.CharField(_("Текст"), max_length=1000, blank=False)
    file = models.FileField(_("Файлы"), upload_to='cars', blank=True)
    color = models.ForeignKey(ColorOfNote, blank=True, default='1')
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.message

from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

# Create your models here.

#
# class Message(models.Model):
#     value = models.CharField(max_length=1000)
#     date = models.DateTimeField(default=datetime.now)
#     user = models.CharField(max_length=1000)
#     room = models.CharField(max_length=1000)
#
#
# class Room(models.Model):
#     name = models.CharField(max_length=250)
#     members = models.ManyToManyField(User, verbose_name=("members"))
#
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class ThreadModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')


class MessageModel(models.Model):
    thread = models.ForeignKey('ThreadModel', related_name='+', on_delete=models.CASCADE, blank=True, null=True)
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    body = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='uploads/message_photos', blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)



from django.db import models
from django.contrib.auth.models import User
from django.http import request
from django.urls import reverse


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post')
    image = models.ImageField(upload_to='post_images/photos/%Y/%m/%d/')
    caption = models.CharField(max_length=250, blank=True, )
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('profile', kwargs={'slug': self.author})

    class Meta:
        ordering = ['-created_at', ]


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='like_post')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liker')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}:{self.post}'

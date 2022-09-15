from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to='profile/photos/%Y/%m/%d/')
    slug = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return str(self.user)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('profile', kwargs={'slug': self.slug})




class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

    def __str__(self):
        return str(self.follower)
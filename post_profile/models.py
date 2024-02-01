from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ProfileDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="userProfile")
    bio = models.CharField(max_length=50, default='No bio')
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/Default_pfp.png', blank=True)


class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploaded_posts/')
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followed_user = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
from django.contrib import admin
from .models import ProfileDetails, Photo

# Register your models here.

class ProfileDetailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'bio', 'profile_picture')

admin.site.register(ProfileDetails, ProfileDetailsAdmin)

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'image', 'caption', 'created_at')

admin.site.register(Photo, PhotoAdmin)
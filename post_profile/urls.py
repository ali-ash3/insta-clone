from django.urls import path
from post_profile import views

app_name = 'post_profile'

urlpatterns = [
    # path('profile/details/<id>', views.add_profile_details, name='profile_details'),
    path('profile/<id>/', views.profile, name='profile'),  
    path('profile/edit/<id>/', views.edit_profile_details, name='edit_profile_details'),
    path('upload_photo/', views.upload_photo, name='upload_photo'), 
    path('photo/<int:photo_id>/', views.photo_detail, name='photo_detail'),
    path('like_photo/<int:photo_id>/', views.like_photo, name='like_photo'),
    path('comment_photo/<int:photo_id>/', views.comment_photo, name='comment_photo'),
    path('follow/<int:user_id>/', views.view_follow, name='toggle_follow'),
    
]
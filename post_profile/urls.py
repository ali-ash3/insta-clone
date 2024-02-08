from django.urls import path
from post_profile import views

app_name = 'post_profile'

urlpatterns = [
    # path('profile/details/<id>', views.add_profile_details, name='profile_details'),
    path('profile/<id>/', views.profile, name='profile'),  
    path('profile/edit/<id>/', views.edit_profile_details, name='edit_profile_details'),
    path('upload_photo/', views.upload_photo, name='upload_photo'), 
    path('photo/<int:id>/', views.photo_detail, name='photo_detail'),
    path('photo/edit/<int:id>/', views.edit_photo, name='edit_photo'),
    path('photo/delete/<int:id>/', views.delete_photo, name='delete_photo'),
    path('like_photo/<int:id>/', views.like_photo, name='like_photo'),
    path('comment_photo/<int:id>/', views.comment_photo, name='comment_photo'),
    path('follow/<int:id>/', views.follow, name='follow'),
    path('unfollow/<int:id>/', views.unfollow, name='unfollow'),
    path('error/<str:message>/', views.error_page, name='error_page'),


    
]
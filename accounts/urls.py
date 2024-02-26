from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.sign_up, name='sign_up'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('change_password/', views.change_password, name='change_password'),
]

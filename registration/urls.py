from django.urls import path, include
from . import views


app_name = 'registration'
urlpatterns = [
    path("", views.index, name="user_profile"),
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]

from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required



# Create your views here.

@login_required(login_url='/registration/login/')
def index(request):
    return render(request, "registration/index.html")


def signup_view(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('registration:user_profile'))
        return render(request, "registration/signup.html")
    elif request.method == "POST":
        new_user = User.objects.create_user(
            username=request.POST.get('username'),
            email=request.POST.get('email'),
            password=request.POST.get('password'),
        )
        new_user.save()
        return HttpResponseRedirect(reverse('registration:login'))


def login_view(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('registration:user_profile'))
        return render(request, "registration/login.html")
    elif request.method == "POST":
        username = request.POST.get('username') # POST["username"]
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('registration:user_profile'))
        else:
            return render(request, "registration/login.html", {"login_message": "Username/password is incorrect"})
        

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('registration:login'))

# views.py
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from post_profile.models import Follow, Photo



@login_required(login_url='accounts:login')
def index(request):
    followed_users = Follow.objects.filter(followed_by=request.user).values_list('followed_to', flat=True)
    posts = Photo.objects.filter(user__in=followed_users).order_by('-created_at')
    return render(request, 'accounts/index.html', {'posts': posts})


def sign_up(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('accounts:index')) 
        return render(request, "accounts/sign_up.html")
    elif request.method == "POST":
        user = User.objects.create_user(
            username=request.POST.get('username'),
            email=request.POST.get('email'),
            password=request.POST.get('password'),
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name')
        )

        # Debugging prints
        print("New user created:", user.username)
        print("New user ID:", user.id)

        # Redirect to edit_profile_details with user's id
        return HttpResponseRedirect(reverse('post_profile:edit_profile_details', kwargs={'id': user.id}))


def login_view(request):
    next_url = request.GET.get('next', '')  # Capture the 'next' parameter from the GET request

    if request.method == "GET":
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('accounts:index')) 
        return render(request, "accounts/log_in.html", {'next_url': next_url})  # Pass 'next_url' to the context
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.POST.get('next', '')  # Make sure to capture the 'next' parameter from the POST request as well

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(next_url) if next_url else redirect('accounts:index')
        else:
            return render(request, "accounts/log_in.html", {"login_message": "Username/password is incorrect", 'next_url': next_url})  # Pass 'next_url' to the context again in case of failure



def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('accounts:login')) 


@login_required(login_url='accounts:login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        user = request.user
        
        if user.check_password(current_password):
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('accounts:change_password')
        else:
            messages.error(request, 'Current password is incorrect.')
            return redirect('accounts:change_password')
    return render(request, 'accounts/change_password.html')


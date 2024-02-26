# views.py
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash


@login_required(login_url='accounts:login')
def index(request):
    all_users = User.objects.all()
    context = {
        'all_users': all_users
    }
    return render(request, "accounts/index.html", context)


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

        profile_id = user.id
        return HttpResponseRedirect(reverse('accounts:index')) 

def login_view(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('accounts:index')) 
        return render(request, "accounts/log_in.html")
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('accounts:index')) 
        else:
            return render(request, "accounts/log_in.html", {"login_message": "Username/password is incorrect"})


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

# @login_required
# def edit_profile(request):
#     user_profile, created = UserProfile.objects.get_or_create(user=request.user)

#     if request.method == 'POST':
#         # Use the existing UserProfile instance or the newly created one
#         form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
#         if form.is_valid():
#             form.save()
#             return redirect('user_profile:view_profile')
#     else:
#         form = UserProfileForm(instance=user_profile)
#     return render(request, 'user_profile/edit_profile.html', {'form': form})


# @login_required
# def view_profile(request):
#     user_profile, created = UserProfile.objects.get_or_create(user=request.user)
#     return render(request, 'user_profile/view_profile.html', {'user_profile': user_profile})



# def index_view (request):
#     UserProfile = UserProfileForm()
#     return render(request, 'user_profile/index.html', { 'form': UserProfile })

# @login_required
# def form_submit(request):
#     form = UserProfileForm(request.POST)
#     if form.is_valid():
#         form.save()
#         return render(request, 'user_profile/view_profile.html', {})
#     else:
#         return render(request, 'user_profile/index.html', {'form': form})

# @login_required
# def view_follow(request):
#     user_profile, created = UserProfile.objects.get_or_create(user=request.user)

#     if request.method == 'POST':
#         follow_form = FollowForm(request.POST)
#         if follow_form.is_valid():
#             user_to_follow_id = follow_form.cleaned_data['user_to_follow']
#             user_to_follow = get_object_or_404(UserProfile, id=user_to_follow_id).user

#             if user_to_follow != request.user:
#                 if user_to_follow in user_profile.followers.all():
#                     user_profile.followers.remove(user_to_follow)
#                 else:
#                     user_profile.followers.add(user_to_follow)

#             return redirect('user_profile:view_profile')
#     else:
#         follow_form = FollowForm()

#     return render(request, 'user_profile/view_profile.html', {'user_profile': user_profile, 'follow_form': follow_form})
    
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from post_profile.models import Comment, Like, Photo, ProfileDetails
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.


@login_required
def edit_profile_details(request, id):
    user = request.user
    profile_details, created = ProfileDetails.objects.get_or_create(user=user)

    if request.method == 'POST':
        bio = request.POST.get('bio', '')
        profile_picture = request.FILES.get('profile_picture', None)

        # Update profile details
        profile_details.bio = bio
        if profile_picture:
            profile_details.profile_picture = profile_picture
        profile_details.save()

        return redirect('post_profile:profile', id=user.id)
    else:
        context = {
            'user': user,
            'profile_details': profile_details,
        }
        return render(request, 'post_profile/edit_profile_details.html', context)



def profile(request, id):
    user = User.objects.get(id=id)
    profile_details ,created = ProfileDetails.objects.get_or_create(user=user)

    # profile_details = ProfileDetails.objects.get(id=)
    context = {
        'user': user,
        'profile_details': profile_details,
    }
    return render(request, 'post_profile/profile.html', context)



@login_required
def upload_photo(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        caption = request.POST.get('caption', '')

        # Create Photo instance
        photo = Photo.objects.create(user=request.user, image=image, caption=caption)
        # photo = Photo(user=request.user, image=image, caption=caption)
        # photo.save()

        # return redirect('interact:photo_detail', photo_id=photo.pk)
        return redirect('post_profile:profile', id=request.user.id)

    return render(request, 'post_profile/upload_photo.html')


@login_required
def like_photo(request, photo_id):
    photo = get_object_or_404(Photo, pk=photo_id)
    user = request.user
    like, created = Like.objects.get_or_create(photo=photo, user=user)

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    like_count = Like.objects.filter(photo=photo).count()

    response_data = {
        'liked': liked,
        'count': like_count,
    }

    # Ensure the content type is set to application/json
    return JsonResponse(response_data)



# @login_required
def comment_photo(request, photo_id):
    photo = get_object_or_404(Photo, pk=photo_id)
    if request.method == 'POST':
        text = request.POST.get('comment_text')
        Comment.objects.create(user=request.user, photo=photo, text=text)
    return redirect('post_profile:photo_detail', photo_id=photo_id)


def photo_detail(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    liked = True if Like.objects.filter(photo=photo, user=request.user).count() > 0 else False
    count = Like.objects.filter(photo=photo).count()
    return render(request, 'post_profile/photo_detail.html', {'photo': photo, 'liked': liked, 'count': count})

@login_required
def view_follow(request, user_id):
    user_to_follow = User.objects.get(id=user_id)

    if user_to_follow != request.user:
        user_profile, created = ProfileDetails.objects.get_or_create(user=request.user)
        
        if user_to_follow in user_profile.following.all():  # Check the user's following list
            user_profile.following.remove(user_to_follow)  # Remove the user from following list
            is_following = False
        else:
            user_profile.following.add(user_to_follow)  # Add the user to following list
            is_following = True
        
        follower_count = user_to_follow.profiledetails.followers.count()  # Get follower count of the followed user

        return JsonResponse({'is_following': is_following, 'follower_count': follower_count})
    else:
        return JsonResponse({'error': 'You cannot follow/unfollow yourself'})


# def add_profile_details(request, id):
    
#     if not request.user.is_authenticated:
#         return redirect('accounts:login')

#     if request.method == 'POST':
#         bio = request.POST.get('bio')
#         profile_picture = request.FILES.get('profile_picture')

#         profile_details_instance, created = ProfileDetails.objects.get_or_create(user=request.user)
#         profile_details_instance.bio = bio
#         profile_details_instance.profile_picture = profile_picture
#         profile_details_instance.save()

#         return redirect('accounts:profile')

#     return render(request, 'post_profile/profile_details.html')
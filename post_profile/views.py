from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from post_profile.models import Comment, Follow, Like, Photo, ProfileDetails
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.


def error_page(request, message):
    return render(request, 'error.html', {'error_message': message})


@login_required(login_url='accounts:login')
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


@login_required(login_url='accounts:login')
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


@login_required(login_url='accounts:login')
def like_photo(request, id):
    photo = get_object_or_404(Photo, pk=id)
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


@login_required(login_url='accounts:login')
def comment_photo(request, id):
    photo = get_object_or_404(Photo, pk=id)
    if request.method == 'POST':
        text = request.POST.get('comment_text')
        Comment.objects.create(user=request.user, photo=photo, text=text)
    return redirect('post_profile:photo_detail', id=id)


@login_required(login_url='accounts:login')
def photo_detail(request, id):
    photo = get_object_or_404(Photo, id=id)
    liked = True if Like.objects.filter(photo=photo, user=request.user).count() > 0 else False
    count = Like.objects.filter(photo=photo).count()
    comments = Comment.objects.filter(photo=photo).order_by('-created_at')
    return render(request, 'post_profile/photo_detail.html', {'photo': photo, "comment": comments, 'liked': liked, 'count': count})


@login_required
def edit_photo(request, id):
    photo = get_object_or_404(Photo, id=id)

    if request.user != photo.user:
        error_message = "You do not have permission to edit this photo."
        return HttpResponseRedirect(reverse('error_page', args=[error_message]))

    if request.method == 'POST':
        new_caption = request.POST.get('caption', '')
        photo.caption = new_caption
        photo.save()
        return HttpResponseRedirect(reverse('post_profile:photo_detail', args=[id]))
    return render(request, 'post_profile/edit_photo.html', {'photo': photo})


@login_required
def delete_photo(request, id):
    photo = get_object_or_404(Photo, pk=id)
    print("photo id: ", photo.pk)
    print('user id', photo.user.id)

    if request.user != photo.user:
        error_message = "You do not have permission to delete this photo."
        return HttpResponseRedirect(reverse('error_page', args=[error_message]))

    if request.method == 'POST':
        photo.delete()
        print("this worked")
        return HttpResponseRedirect(reverse('post_profile:profile', args=[request.user.id]))
    print("photo not deleted")
    return HttpResponseRedirect(reverse('post_profile:photo_detail', args=[id]))


@login_required(login_url='accounts:login')
def follow(request, id):
    user_follow = User.objects.filter(id = id).first()
    follow = Follow.objects.filter(followed_to=user_follow, followed_by=request.user).first()
    if not follow:
        follow_model = Follow.objects.create(followed_to= user_follow, followed_by=request.user)
        follow_model.save()
        return redirect("post_profile:profile", id=id)
    # else:
    #     messages.warning(request, f"already followed")


@login_required(login_url='accounts:login')
def unfollow(request, id):
    user_to_unfollow = get_object_or_404(User, id=id)
    follow = Follow.objects.filter(followed_to=user_to_unfollow, followed_by=request.user).first()
    
    if follow:
        follow.delete()
    return redirect("post_profile:profile", id=id)


@login_required(login_url='accounts:login')
def profile(request, id):
    user = request.user
    user_data = User.objects.filter(id = id).first()
    if user_data is not None:
        if request.user.is_authenticated:
            follow = Follow.objects.filter(followed_by=user, followed_to=user_data).first()
            follower = Follow.objects.filter(followed_to=user_data).count()
            following = Follow.objects.filter(followed_by = user_data).count()
            profile = ProfileDetails.objects.filter(user = user).first()
            profile_data = ProfileDetails.objects.filter(user = user_data).first()
            posts = Photo.objects.filter(user = user_data).order_by('-created_at')
            post_number = posts.count()
            return render(request, "post_profile/profile.html", {"user": user, "profile": profile, "posts": posts, "user_data": user_data, "profile_data": profile_data, "follow": follow, "following": following, "follower": follower, "post_number": post_number})
        return redirect('accounts:login')
    else:
        return render(request, "post_profile/user_not_found.html")
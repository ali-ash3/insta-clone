from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='/registration/login')
def feed(request):
    return render(request, "feed/feed.html")
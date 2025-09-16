from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm, CustomUserCreationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Create your views here.
def index(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            post.save()
            return redirect("index")
    else:
        form = PostForm()
        
    posts = Post.objects.all().order_by("-created_at")
    return render(request, "social/index.html", {"posts": posts, "form": form})

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/signup.html", {"form": form})
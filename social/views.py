from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm, CustomUserCreationForm, UserUpdateForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

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

@login_required
def edit_profile(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = UserUpdateForm(instance=request.user)
            
    return render(request, "social/edit_profile.html", {"form": form})
    
@login_required
def profile(request):
    return render(request, "social/profile.html", {"user": request.user})
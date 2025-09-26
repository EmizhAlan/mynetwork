from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Like
from .forms import PostForm, CustomUserCreationForm, UserUpdateForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

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

User = get_user_model()

def user_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    return render(request, "social/user_profile.html", {"profile_user": profile_user})

@login_required
def toggle_like(request, post_id):
    if request.method == "POST":
        post = Post.objects.get(id=post_id)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()
            liked = False
        else:
            liked = True
        return JsonResponse({
            'liked': liked,
            'likes_count': post.likes.count()
        })
    return JsonResponse({"error": "Неверный метод"}, status=400)
    
@login_required
def feed(request):
    posts = Post.objects.all().order_by('-created_at')
    for post in posts:
        post.liked_by_user = post.likes.filter(user=request.user).exists()
    return render(request, 'social/feed.html', {'posts': posts})
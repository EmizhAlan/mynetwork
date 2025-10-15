from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Like, Comment, Friendship, User, Message
from .forms import PostForm, CustomUserCreationForm, UserUpdateForm, SignupForm, MessageForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django.contrib import messages

# Create your views here.

User = get_user_model()

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

    # Добавляем флаг liked_by_user для каждого поста
    if request.user.is_authenticated:
        for post in posts:
            post.liked_by_user = post.is_liked_by(request.user)
    else:
        for post in posts:
            post.liked_by_user = False

    return render(request, "social/index.html", {"posts": posts, "form": form})

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})


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

@login_required
def user_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    friendship = Friendship.objects.filter(
        Q(from_user=request.user, to_user=profile_user) | 
        Q(from_user=profile_user, to_user=request.user)
    ).first()

    friendship_status = "none"
    friendship_id = None

    if friendship:
        friendship_id = friendship.id
        if friendship.status == "accepted":
            friendship_status = "friends"
        elif friendship.from_user == request.user:
            friendship_status = "pending"
        elif friendship.to_user == request.user and friendship.status == "pending":
            friendship_status = "incoming"

    return render(request, "social/user_profile.html", {
        "profile_user": profile_user,
        "friendship_status": friendship_status,
        "friendship_id": friendship_id
    })

@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({
        "liked": liked,
        "likes_count": Like.objects.filter(post=post).count(),
    })
    
@login_required
def feed(request):
    posts = Post.objects.all().order_by('-created_at')
    for post in posts:
        post.liked_by_user = post.likes.filter(user=request.user).exists()
    return render(request, 'social/feed.html', {'posts': posts})

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST" and request.user.is_authenticated:
        content = request.POST.get("content")
        if content:
            Comment.objects.create(post=post, user=request.user, content=content)
    return redirect("index")

@login_required(login_url="login")
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            Comment.objects.create(user=request.user, post=post, content=content)
            return redirect("post_detail", post_id=post.id)

    comments = post.comments.all()
    return render(request, "social/post_detail.html", {"post": post, "comments": comments})

@login_required
def send_friend_request(request, username):
    to_user = get_object_or_404(User, username=username)
    if to_user == request.user:
        messages.warning(request, "Нельзя отправить запрос самому себе.")
        return redirect('user_profile', username=username)

    friendship, created = Friendship.objects.get_or_create(from_user=request.user, to_user=to_user)
    if created:
        friendship.status = 'pending'
        friendship.save()
        messages.success(request, "Запрос в друзья отправлен.")
    else:
        # уже есть запись
        if friendship.status == 'pending':
            messages.info(request, "Запрос уже отправлен и ожидает подтверждения.")
        elif friendship.status == 'accepted':
            messages.info(request, "Вы уже друзья.")
        elif friendship.status == 'rejected':
            friendship.status = 'pending'
            friendship.save()
            messages.success(request, "Запрос отправлен заново.")
    return redirect('user_profile', username=username)

@login_required
def accept_friend_request(request, friendship_id):
    friendship = get_object_or_404(Friendship, id=friendship_id, to_user=request.user)
    if request.method == "POST":
        friendship.status = 'accepted'
        friendship.save()
        messages.success(request, f"Вы приняли заявку от {friendship.from_user.username}.")
        return redirect('friend_requests')
    # если GET — просто перенаправляем
    return redirect('friend_requests')

@login_required
def reject_friend_request(request, friendship_id):
    friendship = get_object_or_404(Friendship, id=friendship_id, to_user=request.user)
    if request.method == "POST":
        friendship.status = 'rejected'
        friendship.save()
        messages.info(request, "Заявка отклонена.")
        return redirect('friend_requests')
    return redirect('friend_requests')

@login_required
def friend_requests(request):
    # Входящие заявки
    incoming = Friendship.objects.filter(to_user=request.user, status='pending')
    
    # Исходящие заявки
    outgoing = Friendship.objects.filter(from_user=request.user, status='pending')
    
    return render(request, 'social/friend_requests.html', {
        'incoming_requests': incoming,
        'outgoing_requests': outgoing,
    })
    
@login_required
def cancel_friend_request(request, friendship_id):
    friendship = get_object_or_404(Friendship, id=friendship_id, from_user=request.user, status='pending')
    if request.method == "POST":
        friendship.delete()
        messages.info(request, "Запрос в друзья отменён.")
    return redirect('friend_requests')

@login_required
def feed(request):
    friends = Friendship.objects.filter(
        (Q(from_user=request.user) | Q(to_user=request.user)),
        status='accepted'
    )
    friend_ids = set()
    for f in friends:
        if f.from_user != request.user:
            friend_ids.add(f.from_user.id)
        if f.to_user != request.user:
            friend_ids.add(f.to_user.id)

    posts = Post.objects.filter(autor__id__in=friend_ids).order_by('-created_at')
    for post in posts:
        post.liked_by_user = post.likes.filter(user=request.user).exists()
    return render(request, 'social/feed.html', {'posts': posts})

@login_required
def friends_list(request):
    friendships = Friendship.objects.filter(
        (Q(from_user=request.user) | Q(to_user=request.user)),
        status='accepted'
    )

    friends = []
    for f in friendships:
        if f.from_user == request.user:
            friends.append(f.to_user)
        else:
            friends.append(f.from_user)

    return render(request, 'social/friends_list.html', {'friends': friends})

@login_required
def remove_friend(request, username):
    other = get_object_or_404(User, username=username)
    friendship = Friendship.objects.filter(
        (Q(from_user=request.user, to_user=other) | Q(from_user=other, to_user=request.user)),
        status='accepted'
    ).first()
    if friendship:
        friendship.delete()
        messages.success(request, f"{other.username} удалён(а) из друзей.")
    return redirect('user_profile', username=username)

@login_required
def conversations(request):
    # Получаем всех пользователей, с которыми есть переписка
    user_ids = Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user))\
                .values_list('sender', 'receiver')
                
    chat_user_ids = set()
    for s_id, r_id in user_ids:
        if s_id != request.user.id:
            chat_user_ids.add(s_id)
        if r_id != request.user.id:
            chat_user_ids.add(r_id)
            
    users = User.objects.filter(id__in=chat_user_ids)
    return render(request, 'social/conversations.html', {'users': users})

@login_required
def chat(request, username):
    other_user = get_object_or_404(User, username=username)
    messages = Message.objects.filter(
        (Q(sender=request.user, receiver=other_user) | Q(sender=other_user, receiver=request.user))
    ).order_by('created_at')
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = other_user
            message.save()
            return redirect('chat', username=username)
    else:
        form = MessageForm()
        
    return render(request, 'social/chat.html', {
        'other_user' : other_user,
        'messages': messages,
        'form': form
    })
    
@login_required
def chat_view(request, username):
    other_user = get_object_or_404(User, username=username)
    messages = Message.objects.filter(
        (Q(sender=request.user, receiver=other_user) |
         Q(sender=other_user, receiver=request.user))
    ).order_by('created_at')

    if request.method == 'POST':
        content = request.POST.get('content')
        if content.strip():
            Message.objects.create(sender=request.user, receiver=other_user, content=content)
            return redirect('chat_view', username=username)

    return render(request, 'social/chat.html', {
        'other_user': other_user,
        'messages': messages,
    })
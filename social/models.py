from django.contrib.auth.models import AbstractUser, User
from django.db import models

# Create your models here.
class User(AbstractUser):
    bio = models.TextField(blank=True, null=True, verbose_name="О себе")
    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True,
        default="avatars/test.png",  # обязательно в media/
        verbose_name="Аватар"
    )

    def __str__(self):
        return self.username
    
class Post(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    image = models.ImageField(upload_to="posts/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return f"{self.autor} - {self.created_at:%Y-%m-%d %H:%M}"
    
    def is_liked_by(self, user):
        return self.likes.filter(user=user).exists()
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'post')
        
    def __str__(self):
        return f"{self.user.username} liked {self.post.id}"
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} on {self.post.id}: {self.content[:20]}"
    
class Friendship(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friandships_sent")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships_received')
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ("from_user", "to_user")
        
    def __str__(self):
        return f"{self.from_user.username} -> {self.to_user.username} ({self.status})"
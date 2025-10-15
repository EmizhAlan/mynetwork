from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Post, Like, Comment, Friendship, Message

User = get_user_model()

class SocialTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username="user1", password="12345")
        self.user2 = User.objects.create_user(username="user2", password="12345")
        self.post = Post.objects.create(autor=self.user1, content="Test post")

    def test_signup(self):
        response = self.client.post(reverse("signup"), {
            "username": "newuser",
            "password1": "ComplexPass123",
            "password2": "ComplexPass123"
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_login_and_create_post(self):
        self.client.login(username="user1", password="12345")
        response = self.client.post(reverse("index"), {
            "content": "New post"
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(content="New post").exists())

    def test_like_unlike_post(self):
        self.client.login(username="user2", password="12345")
        url = reverse("toggle_like", args=[self.post.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Like.objects.filter(user=self.user2, post=self.post).exists())
        # Unlike
        self.client.post(url)
        self.assertFalse(Like.objects.filter(user=self.user2, post=self.post).exists())

    def test_add_comment(self):
        self.client.login(username="user2", password="12345")
        url = reverse("add_comment", args=[self.post.id])
        response = self.client.post(url, {"content": "Nice!"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(content="Nice!").exists())

    def test_send_and_accept_friend_request(self):
        self.client.login(username="user1", password="12345")
        url = reverse("send_friend_request", args=[self.user2.username])
        self.client.post(url)
        friendship = Friendship.objects.get(from_user=self.user1, to_user=self.user2)
        self.assertEqual(friendship.status, "pending")

        self.client.logout()
        self.client.login(username="user2", password="12345")
        accept_url = reverse("accept_friend_request", args=[friendship.id])
        self.client.post(accept_url)
        friendship.refresh_from_db()
        self.assertEqual(friendship.status, "accepted")
        
    def test_send_message(self):
        self.client.login(username="user1", password=12345)
        url = reverse('chat', args=[self.user2.username])
        response = self.client.post(url, {"content": "Привет!"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Message.objects.filter(sender=self.user1, receiver=self.user2, content="Привет!").exists())

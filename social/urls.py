from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path("profile/", views.profile, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("logout/", auth_views.LogoutView.as_view(template_name="logout.html"), name='logout'),

    # user & posts
    path("user/<str:username>/", views.user_profile, name="user_profile"),
    path("post/<int:post_id>/like/", views.toggle_like, name="toggle_like"),
    path("post/<int:post_id>/comment/", views.add_comment, name="add_comment"),
    path("post/<int:post_id>/", views.post_detail, name="post_detail"),

    # friends / requests
    path("friends/", views.friends_list, name="friends_list"),
    path("friend-requests/", views.friend_requests, name="friend_requests"),
    path("friend-request/send/<str:username>/", views.send_friend_request, name="send_friend_request"),
    path("friend-request/<int:friendship_id>/accept/", views.accept_friend_request, name="accept_friend_request"),
    path("friend-request/<int:friendship_id>/reject/", views.reject_friend_request, name="reject_friend_request"),
    path("friend/remove/<str:username>/", views.remove_friend, name="remove_friend"),
    
    # обработка логотипа для админки
    path('favicon.ico', RedirectView.as_view(url='/static/social/images/logo.png')),
]

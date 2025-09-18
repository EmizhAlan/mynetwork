from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path("profile/", views.profile, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("logout/", auth_views.LogoutView.as_view(template_name="logout.html"), name='logout'),
    path("user/<str:username>/", views.user_profile, name="user_profile"),
]

from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.accounts_home, name="home"),
    path("sign/", views.sign, name="sign"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("profile/", views.profile_view, name="profile"),
    path("settings/", views.settings_view, name="settings"),
]

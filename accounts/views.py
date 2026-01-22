from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm

from .models import Profile
from .forms import (
    ProfileForm,
    ProfileUpdateForm,
    UserUpdateForm,
    EmailUpdateForm,
)


@login_required
def settings_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "change_email":
            email_form = EmailUpdateForm(request.POST, instance=request.user)
            if email_form.is_valid():
                email_form.save()
                messages.success(request, "Email updated successfully")
                return redirect("accounts:settings")
            messages.error(request, "Invalid email address")

        elif action == "update_profile":
            user_form = UserUpdateForm(request.POST, instance=request.user)
            profile_form = ProfileForm(request.POST, request.FILES, instance=profile)

            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, "Profile updated successfully")
                return redirect("accounts:settings")
            messages.error(request, "Please check the form fields")

        elif action == "change_password":
            pass_form = PasswordChangeForm(user=request.user, data=request.POST)
            if pass_form.is_valid():
                user = pass_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Password changed successfully")
                return redirect("accounts:settings")
            messages.error(request, "Password change failed")

    email_form = EmailUpdateForm(instance=request.user)
    user_form = UserUpdateForm(instance=request.user)
    profile_form = ProfileForm(instance=profile)
    pass_form = PasswordChangeForm(user=request.user)

    return render(
        request,
        "accounts/settings.html",
        {
            "email_form": email_form,
            "user_form": user_form,
            "profile_form": profile_form,
            "pass_form": pass_form,
            "profile": profile,
        },
    )


def sign(request):
    if request.method == "POST":
        username = (request.POST.get("username") or "").strip()
        email = (request.POST.get("email") or "").strip()
        password = request.POST.get("password") or ""
        password2 = request.POST.get("password2") or ""

        if not username:
            return render(request, "accounts/sign.html", {"error": "Username is required"})
        if not password:
            return render(request, "accounts/sign.html", {"error": "Password is required"})
        if password != password2:
            return render(request, "accounts/sign.html", {"error": "Passwords do not match"})

        if User.objects.filter(username=username).exists():
            return render(request, "accounts/sign.html", {"error": "Username already exists"})

        if email and User.objects.filter(email=email).exists():
            return render(request, "accounts/sign.html", {"error": "Email already exists"})

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        login(request, user)
        messages.success(request, "Account created successfully")

        next_url = request.GET.get("next")
        return redirect(next_url or "accounts:profile")

    return render(request, "accounts/sign.html")


def user_login(request):
    if request.method == "POST":
        username = (request.POST.get("username") or "").strip()
        password = request.POST.get("password") or ""

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Welcome back")

            next_url = request.GET.get("next")
            return redirect(next_url or "accounts:profile")

        return render(request, "accounts/login.html", {"error": "Invalid credentials"})

    return render(request, "accounts/login.html")


def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out")
    return redirect("accounts:login")


@login_required
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully")
            return redirect("accounts:profile")
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(
        request,
        "accounts/profile.html",
        {
            "form": form,
            "profile": profile,
        }
    )


def accounts_home(request):
    return render(request, "accounts/home.html")

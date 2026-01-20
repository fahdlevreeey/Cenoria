from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username"]
        labels = {
            "username": "Username",
        }

    def clean_username(self):
        username = (self.cleaned_data.get("username") or "").strip()
        qs = User.objects.filter(username__iexact=username).exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("This username is already taken.")
        return username


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["photo"]
        labels = {
            "photo": "Profile photo",
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("bio",)

class EmailUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email"]
        labels = {"email": "Email"}

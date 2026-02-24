from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import User, Talk


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email",)

class LoginForm(AuthenticationForm):
    pass

class TalkForm(forms.ModelForm):
    class Meta:
        model = Talk
        fields = ("message",)
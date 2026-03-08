from django import forms
from .models import User


class SignupForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "phone", "password"]


class LoginForm(forms.Form):

    email = forms.EmailField()

    password = forms.CharField(widget=forms.PasswordInput)


class PhoneForm(forms.Form):

    phone = forms.CharField(max_length=15)


class OTPForm(forms.Form):

    otp = forms.CharField(max_length=6)


class ResetPasswordForm(forms.Form):

    password = forms.CharField(widget=forms.PasswordInput)
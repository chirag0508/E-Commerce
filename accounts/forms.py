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
    password = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={"placeholder": "New password"}),
        min_length=8,
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm new password"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")
        if password and confirm and password != confirm:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

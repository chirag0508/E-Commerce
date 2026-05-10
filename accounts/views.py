from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
import random

from .forms import SignupForm, LoginForm, OTPForm, ResetPasswordForm
from .models import User, OTP


# ─── SIGNUP ────────────────────────────────────────────────────────────────────

def signup(request):
    form = SignupForm()
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, "Account created successfully")
            return redirect("home")
        else:
            messages.error(request, "Please correct the errors below")
    return render(request, "signup.html", {"form": form})


# ─── LOGIN / LOGOUT ─────────────────────────────────────────────────────────────

def user_login(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None
            if user and user.check_password(password):
                login(request, user)
                messages.success(request, "Login successful")
                return redirect("home")
            else:
                messages.error(request, "Invalid email or password")
    return render(request, "login.html", {"form": form})


def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect("home")


# ─── PHONE OTP LOGIN ────────────────────────────────────────────────────────────

def phone_login(request):
    from .forms import PhoneForm
    form = PhoneForm()
    if request.method == "POST":
        form = PhoneForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data["phone"]
            otp = random.randint(100000, 999999)
            OTP.objects.create(phone=phone, otp=otp)
            request.session["phone"] = phone
            print("OTP:", otp)
            messages.success(request, "OTP sent. Check terminal.")
            return redirect("verify_otp")
    return render(request, "phone.html", {"form": form})


def verify_otp(request):
    form = OTPForm()
    phone = request.session.get("phone")
    if request.method == "POST":
        form = OTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data["otp"]
            record = OTP.objects.filter(phone=phone, otp=otp).last()
            if record:
                user = User.objects.filter(phone=phone).first()
                if not user:
                    user = User.objects.create(username=phone, phone=phone)
                login(request, user)
                messages.success(request, "Login successful")
                return redirect("home")
            else:
                messages.error(request, "Invalid OTP")
    return render(request, "otp.html", {"form": form})


# ─── FORGOT PASSWORD (EMAIL OTP) ────────────────────────────────────────────────

def forgot_password(request):
    """Step 1 – enter email, receive OTP."""
    error = None
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            error = "No account found with that email address."
            return render(request, "forgot.html", {"error": error})

        otp = random.randint(100000, 999999)
        request.session["reset_email"] = email
        request.session["reset_otp"] = str(otp)

        send_mail(
            subject="Password Reset OTP – Your Shop",
            message=(
                f"Hello {user.username},\n\n"
                f"Your OTP for password reset is: {otp}\n\n"
                "This OTP is valid for this session only.\n"
                "If you did not request this, ignore this email."
            ),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )
        messages.success(request, "OTP sent to your email address.")
        return redirect("verify_reset_otp")

    return render(request, "forgot.html")


def verify_reset_otp(request):
    """Step 2 – enter OTP received by email."""
    if request.method == "POST":
        user_otp = request.POST.get("otp", "").strip()
        session_otp = request.session.get("reset_otp", "")

        if user_otp and user_otp == session_otp:
            # Mark OTP as verified so reset_password knows it's safe
            request.session["otp_verified"] = True
            return redirect("reset_password")
        else:
            return render(request, "verify_reset_otp.html", {"error": "Invalid OTP. Please try again."})

    return render(request, "verify_reset_otp.html")


def reset_password(request):
    """Step 3 – set a new password."""
    # Guard: only accessible after OTP verified
    if not request.session.get("otp_verified"):
        messages.error(request, "Please verify your OTP first.")
        return redirect("forgot_password")

    email = request.session.get("reset_email")

    if request.method == "POST":
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data["password"]
            confirm = form.cleaned_data["confirm_password"]

            if password != confirm:
                messages.error(request, "Passwords do not match.")
                return render(request, "reset_password.html", {"form": form})

            UserModel = get_user_model()
            try:
                user = UserModel.objects.get(email=email)
            except UserModel.DoesNotExist:
                messages.error(request, "Session expired. Please start again.")
                return redirect("forgot_password")

            user.set_password(password)
            user.save()

            # Clean up session keys
            for key in ("reset_email", "reset_otp", "otp_verified"):
                request.session.pop(key, None)

            messages.success(request, "Password reset successful. Please log in.")
            return redirect("login")
    else:
        form = ResetPasswordForm()

    return render(request, "reset_password.html", {"form": form})

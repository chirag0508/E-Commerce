from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import SignupForm, LoginForm, PhoneForm, OTPForm
from .models import User, OTP
import random
from .forms import SignupForm, LoginForm, PhoneForm, OTPForm, ResetPasswordForm
import random
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

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


def phone_login(request):

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
def forgot_password(request):

    form = PhoneForm()

    if request.method == "POST":

        form = PhoneForm(request.POST)

        if form.is_valid():

            phone = form.cleaned_data["phone"]

            if not User.objects.filter(phone=phone).exists():

                messages.error(request, "Account with this phone does not exist")

                return redirect("forgot_password")

            otp = random.randint(100000, 999999)

            OTP.objects.create(phone=phone, otp=otp)

            request.session["reset_phone"] = phone

            print("RESET OTP:", otp)

            messages.success(request, "OTP sent. Check terminal.")

            return redirect("verify_reset_otp")

    return render(request, "forgot.html", {"form": form})

def verify_reset_otp(request):

    if request.method == "POST":

        user_otp = request.POST.get("otp")
        session_otp = request.session.get("reset_otp")

        if user_otp == session_otp:
            return redirect("reset_password")

        else:
            return render(request, "verify_reset_otp.html", {"error": "Invalid OTP"})

    return render(request, "verify_reset_otp.html")

def reset_password(request):

    email = request.session.get("reset_email")

    if request.method == "POST":

        password = request.POST.get("password")
        confirm = request.POST.get("confirm_password")

        if password != confirm:
            messages.error(request, "Passwords do not match")
            return redirect("reset_password")

        user = User.objects.get(email=email)

        user.set_password(password)
        user.save()

        messages.success(request, "Password reset successful")

        return redirect("login")

    return render(request, "reset_password.html")

def forgot_password(request):

    if request.method == "POST":

        email = request.POST.get("email")

        User = get_user_model()

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, "forgot.html", {"error": "Email not found"})

        otp = random.randint(100000, 999999)

        request.session["reset_email"] = email
        request.session["reset_otp"] = str(otp)

        send_mail(
            "Password Reset OTP",
            f"Your OTP is {otp}",
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        return redirect("verify_reset_otp")

    return render(request, "forgot.html")
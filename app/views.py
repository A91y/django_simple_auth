from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from .utils import is_valid_email
# Create your views here.


def home(request: HttpRequest):
    return render(request, "home.html", context={"name": "home"})


def login_view(request: HttpRequest):
    if request.user.is_authenticated:
        messages.info(request, "Already, logged in...")
        return redirect("home")
    if request.method == "POST":
        email: str = request.POST.get("email", "")
        password: str = request.POST.get("password", "")

        if not email or not password:
            messages.error(request, "Please fill out all required fields...")
            return redirect("login")

        if not is_valid_email(email):
            messages.error(request, "Please provide a valid email address...")
            return redirect("login")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Successfully! Logged in.")
            return redirect("dashboard")
        messages.error(request, "Incorrect Email or Password...")
        return redirect("login")

    return render(request, "login.html", context={"name": "login"})


def register_view(request: HttpRequest):
    if request.user.is_authenticated:
        messages.info(request, "Already, logged in...")
        return redirect("home")
    if request.method == "POST":
        first_name: str = request.POST.get("fname", None)
        last_name: str = request.POST.get("lname", "")
        email: str = request.POST.get("email", None)
        password: str = request.POST.get("password", None)
        if not first_name or not email or not password:
            messages.error(request, "Please fill out all required fields...")
            return redirect("register")
        if not is_valid_email(email):
            messages.error(request, "Please provide a valid email address...")
            return redirect("register")
        if User.objects.filter(email=email).exists():
            messages.info(request, "User with this email already exists...")
            return redirect("home")
        user = User.objects.create_user(
            username=email, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        user = authenticate(request, username=email, password=password)
        login(request, user)
        messages.success(request, "User registered successfully...")
        return redirect("dashboard")
    return render(request, "register.html", context={"name": "register"})


@login_required
def logout_view(request: HttpRequest):
    logout(request)
    messages.success(request, "Logged out...")
    return redirect("home")

@login_required
def dashboard(request: HttpRequest):
    return render(request, "dashboard.html", context={"name": "dashboard"})
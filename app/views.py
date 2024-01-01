from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
# Create your views here.

def index(request: HttpRequest):
    return render(request, "index.html", context={"name": "index"})

def login_view(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == "POST":
        email: str = request.POST.get("email", "")
        password: str = request.POST.get("password", "") 
    return render(request, "login.html", context={"name": "login"})

def register_view(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == "POST":
        first_name: str = request.POST.get("fname", "")
        last_name: str = request.POST.get("lname", "")
        email: str = request.POST.get("email", "")
        password: str = request.POST.get("password", "")
    return render(request, "register.html", context={"name": "register"})

@login_required
def logout_view(request: HttpRequest):
    logout(request)
    return redirect("index")
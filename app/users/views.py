import uuid

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from verify_email.email_handler import send_verification_email

from .forms import RegisterForm, ChangeUserForm
from core.models import Task


User = get_user_model()


def loginPage(request):
    """Login page view."""

    if request.method == "POST":
        email = request.POST["email"].lower()
        password = request.POST["password"]
        try:
            User.objects.get(email=email)
        except ValueError:
            messages.error(request, message="User does not exist.")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "User was logged in successfully.")
            return redirect("my_tasks", pk=user.uuid)
        else:
            messages.error(request, "Email or password is incorrect.")
            return render(request, "users/login.html")

    return render(request, "registration/login.html")


@login_required
def logoutPage(request):
    """Logout page view."""
    user = request.user
    if request.method == "POST":
        logout(request)
        messages.success(request, "You have been logged out.")
        return redirect("home")
    return render(request, "users/logout.html", {"user": user})


def registerPage(request):
    """Register page view."""
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            inactive_user = send_verification_email(request, form)
            messages.success(request, "User has been created successfully.")
            return redirect("register")

    return render(request, "core/index.html", {"form": form})


def profilePage(request, pk):
    """Profile page view."""
    try:
        tasks = Task.objects.select_related("assigned_to").filter(assigned_to__uuid=pk)
        user = tasks.first().assigned_to
        completed_tasks = tasks.filter(status="Completed").count()
        if completed_tasks > 0:
            completed_ontime = (
                100 - tasks.filter(status="Expired").count() // completed_tasks
            )
        else:
            completed_ontime = "N/A"
        tasks_inprogress = tasks.filter(status="In Progress").count()
        tasks_await = tasks.filter(status="Awaits").count()
        skills = user.skills.all()

        context = {
            "user": user,
            "skills": skills,
            "tasks": tasks,
            "completed_tasks": completed_tasks,
            "completed_ontime": completed_ontime,
            "tasks_inprogress": tasks_inprogress,
            "tasks_await": tasks_await,
        }
    except:
        user = get_object_or_404(User, uuid=pk)
        skills = user.skills.all()
        context = {"user": user, "skills": skills}

    return render(request, "users/profile.html", context)


@login_required(login_url="login")
def editProfilePage(request, pk):
    """Edit profile view."""
    if request.user.uuid == uuid.UUID(pk):
        form = ChangeUserForm(instance=request.user)
        if request.method == "POST":
            form = ChangeUserForm(request.POST, request.FILES, instance=request.user)
            if form.is_valid():
                form.save()
                return redirect("profile", pk=pk)
        return render(request, "users/edit_profile1.html", {"form": form})
    else:
        return redirect("home")


@login_required(login_url="login")
def deleteProfile(request, pk):
    if request.user.uuid == pk:
        user = User.objects.get(uuid=pk)
        if request.method == "POST":
            user.delete()
            return redirect("home")
    return render(request, "users/delete_profile.html")

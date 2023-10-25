import uuid

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str


from .forms import RegisterForm, ChangeUserForm, SetPasswordForm
from .tokens import account_activation_token
from .utils import activate_email
from core.models import Task


User = get_user_model()


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(uuid=uid)
    except:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(
            request,
            "Thank you for verifying your email. Now you can login your account.",
        )
        return redirect("login")
    else:
        messages.error(request, "Verification link is invalid.")
        return redirect("register")


def loginPage(request):
    """Login page view."""

    if request.method == "POST":
        email = request.POST["email"].lower()
        password = request.POST["password"]
        user = get_object_or_404(User, email=email)

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
    return render(request, "registration/logout.html", {"user": user})


def registerPage(request):
    """Register page view."""
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activate_email(request, user, form.cleaned_data.get("email"))
            messages.success(request, "User has been created successfully.")
            return redirect("verification_sent")

    return render(request, "core/index.html", {"form": form})


def verification_sent(request):
    """View for verification redirect."""
    return render(request, "registration/verification_sent.html")


def profilePage(request, pk):
    """Profile page view"""

    try:
        tasks = Task.objects.select_related("assigned_to").filter(assigned_to__uuid=pk)
        user = tasks.first().assigned_to
        completed_tasks = tasks.filter(status="Completed").count()
        expired_tasks = tasks.filter(status="Expired").count()
        if completed_tasks > 0:
            completed_ontime = int(100 - expired_tasks // (completed_tasks / 100))

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
        context = {
            "user": user,
            "skills": skills,
        }
    is_friend = False
    if request.user.teammates.filter(uuid=user.uuid).exists():
        is_friend = True
    context["is_friend"] = is_friend

    return render(request, "users/profile.html", context)


@login_required(login_url="login")
def editProfilePage(request, pk):
    """Edit profile view."""
    if request.user.uuid == pk:
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


@login_required(login_url="login")
def add_to_team(request, pk):
    user = User.objects.get(uuid=pk)
    try:
        request.user.teammates.get(uuid=user.uuid)
        return redirect("profile", pk=user.uuid)

    except:
        if request.method == "POST":
            request.user.teammates.add(user)
            return redirect("profile", pk=user.uuid)
    return render(request, "users/profile.html")


@login_required(login_url="login")
def delete_from_team(request, pk):
    user = User.objects.get(uuid=pk)
    if request.user.teammates.get(uuid=user.uuid):
        if request.method == "POST":
            request.user.teammates.remove(user)
            return redirect("profile", pk=user.uuid)
    return render(request, "users/profile.html")


@login_required(login_url="login")
def setPasswordPage(request):
    user = request.user
    form = SetPasswordForm(user)

    if request.method == "POST":
        form = SetPasswordForm(user)
        return redirect("profile", pk=user.uuid)
    return render(request, "registration/reset.html", {"form": form})

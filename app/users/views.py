from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.views.decorators.cache import cache_page
from django.db.models import Count, Q
from django.http import HttpResponse


from .forms import RegisterForm, ChangeUserForm, SetPasswordForm, PasswordResetForm
from .tokens import account_activation_token
from .utils import email_maker, threshold_30
from .tasks import send_email
from tasks.models import Task
from projects.models import Project
from projects.forms import ProjectAddParticipantForm


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
        user = get_object_or_404(User, email__iexact=email)

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "User was logged in successfully.")
            return redirect("my_tasks")
        else:
            messages.error(request, "Email or password is incorrect.")
            return render(request, "registration/login.html")

    return render(request, "registration/login.html")


@login_required(login_url="login")
def logoutPage(request):
    """Logout page view."""

    user = request.user
    if request.method == "POST":
        logout(request)
        messages.success(request, "You have been logged out.")
        return redirect("register")
    return render(request, "registration/logout.html", {"user": user})


def registerPage(request):
    """Register page view."""

    if request.user.is_authenticated:
        return redirect("my_tasks")
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            email_subject = "Email Verification Mail"
            email_template = "emails/activate_account.html"
            message = email_maker(
                request, user, user.email, email_template=email_template
            )
            send_email.delay(email_subject, message, to=[user.email])
            messages.success(request, "User has been created successfully.")
            return redirect("verification_sent")

    return render(request, "core/index.html", {"form": form})


def password_reset(request):
    """View for reset password page."""

    form = PasswordResetForm()
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user = User.objects.filter(email=email).first()
            if user:
                email = user.email
                email_subject = "Password Reset"
                email_template = "emails/reset_password_email.html"
                message = email_maker(
                    request, user, user.email, email_template=email_template
                )
                send_email.delay(email_subject, message, to=[user.email])
                return redirect("password_reset_sent")

    return render(request, "registration/reset_password.html", {"form": form})


def password_reset_message_sent(request):
    return render(request, "registration/reset_password_sent.html")


def password_reset_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(uuid=uid)
    except:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        return redirect("password_reset_complete", pk=user.uuid)
    else:
        messages.error(request, "Verification link is invalid.")
        return redirect("password_reset")


@login_required(login_url="login")
def password_reset_complete(request, pk):
    user = get_object_or_404(User, uuid=pk)
    form = SetPasswordForm(user)
    if request.method == "POST":
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, "Your password has been changed.")
            return redirect("login")
    return render(request, "registration/reset_anonym.html", {"form": form})


def verification_sent(request):
    """View for verification redirect."""
    return render(request, "registration/verification_sent.html")


# @cache_page(60 * 2)
@login_required(login_url="login")
def profilePage(request, pk):
    """Profile page view"""
    utc_now = datetime.utcnow()
    threshold = threshold_30(utc_now)

    completed_tasks = Count(
        "task", filter=Q(task__status="Completed") & Q(task__updated__gt=threshold)
    )
    inprogress_tasks = Count(
        "task", filter=Q(task__status="In Progress") & Q(task__updated__gt=threshold)
    )
    expired_tasks = Count(
        "task", filter=Q(task__status="Expired") & Q(task__updated__gt=threshold)
    )
    await_tasks = Count(
        "task", filter=Q(task__status="Awaits") & Q(task__updated__gt=threshold)
    )

    user = User.objects.annotate(
        completed_tasks=completed_tasks,
        expired_tasks=expired_tasks,
        inprogress_tasks=inprogress_tasks,
        await_tasks=await_tasks,
    ).get(uuid=pk)

    skills = user.skills.all()

    completed_tasks = user.completed_tasks
    expired_tasks = user.expired_tasks
    if completed_tasks > 0:
        completed_ontime = int(100 - expired_tasks // (completed_tasks / 100))
    else:
        completed_ontime = "N/A"
    inprogress_tasks = user.inprogress_tasks
    await_tasks = user.await_tasks

    is_friend = False
    if request.user.teammates.filter(uuid=user.uuid).exists():
        is_friend = True

    projects = Project.objects.filter(owner=request.user).exclude(participants=user)

    add_to_project_form = ProjectAddParticipantForm(
        projects=projects,
    )

    if request.method == "POST":
        add_to_project_form = ProjectAddParticipantForm(request.POST, projects=projects)
        if add_to_project_form.is_valid():
            project_uuid = add_to_project_form.cleaned_data["project"]
            Project.objects.get(uuid=project_uuid).participants.add(user)

            return redirect("profile", pk=pk)

    context = {
        "user": user,
        "skills": skills,
        "completed_tasks": completed_tasks,
        "completed_ontime": completed_ontime,
        "inprogress_tasks": inprogress_tasks,
        "await_tasks": await_tasks,
        "is_friend": is_friend,
        "add_to_project_form": add_to_project_form,
    }

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
        return render(request, "users/edit_profile.html", {"form": form})
    else:
        return redirect("my_tasks")


# @login_required(login_url="login")
# def deleteProfilePage(request, pk):
#     if request.user.uuid == pk:
#         user = User.objects.get(uuid=pk)
#         if request.method == "POST":
#             user.delete()
#             return redirect("home")
#     return render(request, "users/delete_profile.html")


@login_required(login_url="login")
def add_to_team(request, pk):
    """View for adding a user to the team button."""

    user = get_object_or_404(User, uuid=pk)
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
    """View for deleting a user from the team button."""

    user = get_object_or_404(User, uuid=pk)
    if user in request.user.teammates.all():
        if request.method == "POST":
            request.user.teammates.remove(user)
            return redirect("profile", pk=user.uuid)
        else:
            return render(request, "users/profile.html")
    else:
        return redirect("profile", pk=user.uuid)


@login_required(login_url="login")
def setPasswordPage(request):
    """View for changing the password of authorized user."""

    user = request.user
    form = SetPasswordForm(user)

    if request.method == "POST":
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    return render(request, "registration/reset.html", {"form": form})


@login_required(login_url="login")
def myTeamPage(request):
    user = request.user
    teammates = user.teammates.all()
    return render(request, "users/my_team.html", {"teammates": teammates})

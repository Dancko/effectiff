from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import RegisterForm, ChangeForm


def loginPage(request):
    """Login page view."""

    if request.method == "POST":
        email = request.POST["email"].lower()
        password = request.POST["password"]
        try:
            get_user_model().objects.get(email=email)
        except ValueError:
            messages.error(request, message="User does not exist.")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "User was logged in successfully.")
            return redirect("home")
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
    return render(request, "users/logout.html")


def registerPage(request):
    """Register page view."""

    if request.method == "POST":
        email = request.POST["email"]
        username = request.POST["username"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        try:
            get_user_model().objects.get(email=email)
            messages.error(request, "This email is already used.")
        except:
            if password1 == password2:
                user = get_user_model().objects.create_user(
                    email=email, password=password1, name=username
                )

                login(request, user)
                messages.success(request, "User has been created successfully.")
                return redirect("home")

            else:
                messages.error(request, "Passwords do not match.")
                return redirect("home")

    return render(request, "registration/signup.html")


def profilePage(request, pk):
    """Profile page view."""
    user = get_user_model().objects.get(id=pk)
    skills = user.skills.all()
    return render(request, "users/profile.html", {"user": user, "skills": skills})


@login_required(login_url="login")
def editProfilePage(request, pk):
    """Edit profile view."""
    if request.user.id == pk:
        form = ChangeForm(instance=request.user)
        if request.method == "POST":
            form = ChangeForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return redirect("profile", pk=pk)
        return render(request, "users/edit_profile.html", {"form": form})
    return redirect("home")


@login_required(login_url="login")
def deleteProfile(request, pk):
    if request.user.id == pk:
        user = get_user_model().objects.get(id=pk)
        if request.method == "POST":
            user.delete()
            return redirect("home")
    return render(request, "users/delete_profile.html")

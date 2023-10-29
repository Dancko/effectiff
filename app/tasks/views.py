import uuid

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q
from django.views.decorators.cache import cache_page
from django.core.cache import cache

from core.models import Task, Project, Comment
from .forms import (
    TaskCreateForm,
    TaskAddPartiicipantsForm,
    CommentForm,
    TaskCreateFromProjectForm,
)


User = get_user_model()


@login_required(login_url="login")
def myTasksPage(request):
    user = request.user
    cache.set(user.id, user, timeout=600)

    tasks_all = Task.objects.select_related(
        "project", "project__owner", "assigned_to"
    ).filter(Q(project__owner=user) | Q(assigned_to=user))

    cache.set(f"{user.id}_tasks", tasks_all, 600)

    tasks_assigned = cache.get(f"{user.id}_tasks").filter(project__owner=user)
    tasks = cache.get(f"{user.id}_tasks").filter(assigned_to=user)
    context = {
        "tasks": tasks,
        "tasks_assigned": tasks_assigned,
    }
    return render(request, "tasks/my_tasks.html", context)


@login_required(login_url="login")
def taskDetailPage(request, pk):
    user = request.user
    statuses = ["Awaits", "In Progress", "Completed"]

    comments = (
        Comment.objects.select_related("task", "task__project")
        .filter(task__uuid=pk)
        .all()
    )

    if comments:
        task = comments.first().task
    else:
        task = get_object_or_404(Task, uuid=pk)

    task.is_outdated()
    form = CommentForm()
    if user == task.project.owner or task.assigned_to == user:
        if request.method == "POST":
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = user
                comment.task = task
                comment.save()
                return redirect("task_detail", pk=pk)
    context = {
        "task": task,
        "comments": comments,
        "form": form,
        "statuses": statuses,
    }
    return render(request, "tasks/task.html", context)


@login_required(login_url="login")
def taskChangeStatus(request, pk):
    task = get_object_or_404(Task, uuid=pk)
    if request.method == "POST":
        new_status = request.POST["status"]
        task.status = new_status
        task.save()
        return redirect("task_detail", pk=pk)
    return HttpResponse("{'status': 200}")


@login_required(login_url="login")
def taskCreatePage(request):
    """View for creating a task."""
    page = "create"
    user = request.user
    form = TaskCreateForm(user=user)

    if request.method == "POST":
        form = TaskCreateForm(request.POST, user=user)
        if form.is_valid():
            form.save(commit=True)

            return redirect("my_tasks")
    return render(
        request, "tasks/new_task.html", {"form": form, "page": page, "user": user}
    )


@login_required(login_url="login")
def taskCreateFromProject(request, pk):
    """View for creating a task from project page."""
    page = "create"
    project = Project.objects.get(uuid=pk)

    form = TaskCreateFromProjectForm(project=project)
    if request.method == "POST":
        form = TaskCreateFromProjectForm(request.POST, request.FILES, project=project)

        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect("my_projects", pk=request.user.uuid)
    return render(request, "tasks/new_task.html", {"form": form, "page": page})


@login_required(login_url="login")
def taskEditPage(request, pk):
    """View for editting the tasks."""
    page = "edit"
    task = get_object_or_404(Task, uuid=pk)
    if request.user.uuid == task.project.owner.uuid and task.status != "Completed":
        form = TaskCreateForm(instance=task, user=request.user)
        if request.method == "POST":
            form = TaskCreateForm(request.POST, instance=task, user=request.user)
            if form.is_valid():
                form.save()
                return redirect("my_tasks")
    else:
        return redirect("my_tasks")
    return render(request, "tasks/new_task.html", {"page": page, "form": form})


@login_required(login_url="login")
def deleteTaskPage(request, pk):
    """View for deleting a task."""

    task = get_object_or_404(Task, uuid=pk)
    object = task.title
    if task.project.owner == request.user:
        if request.method == "POST":
            task.delete()
            return redirect("my_tasks")
    return render(request, "delete.html", {"task": task, "object": object})


@login_required(login_url="login")
def addMembers(request, pk):
    page = "edit"
    task = Task.objects.select_related("project").get(uuid=pk)
    if task.project.owner == request.user:
        form = TaskAddPartiicipantsForm(instance=task)

        if request.method == "POST":
            form = TaskAddPartiicipantsForm(request.POST, instance=task)
            if form.is_valid():
                form.save()
                return redirect("task_detail", uuid=pk)
        return render(
            request, "tasks/create_update_task.html", {"form": form, "page": page}
        )

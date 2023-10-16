from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from core.models import Task, Project, Comment
from .forms import TaskCreateForm, TaskAddPartiicipantsForm, CommentForm


@login_required(login_url="login")
def myTasksPage(request, pk):
    if not request.user:
        return redirect("home")
    user = get_user_model().objects.get(id=pk)

    tasks_assigned = Task.objects.filter(project__owner=user)
    tasks = Task.objects.filter(assigned_to=user)
    context = {
        "tasks": tasks,
        "tasks_assigned": tasks_assigned,
    }
    return render(request, "tasks/my_tasks.html", context)


@login_required(login_url="login")
def taskDetailPage(request, pk):
    statuses = ["Awaits", "In Progress", "Completed"]
    task = (
        Task.objects.select_related("assigned_to").select_related("project").get(id=pk)
    )
    task.is_outdated()
    comments = Comment.objects.filter(task=task)
    form = CommentForm()
    if request.user == task.project.owner or task.assigned_to == request.user:
        if request.method == "POST":
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
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
    task = get_object_or_404(Task, pk=pk)
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
            return redirect("my_tasks", pk=request.user.id)
    return render(
        request, "tasks/new_task.html", {"form": form, "page": page, "user": user}
    )


@login_required(login_url="login")
def taskEditPage(request, pk):
    """View for editting the tasks."""
    page = "edit"
    task = get_object_or_404(Task, pk=pk)
    if request.user.id == task.project.owner.id:
        form = TaskCreateForm(instance=task, user=request.user)
        if request.method == "POST":
            form = TaskCreateForm(request.POST, instance=task, user=request.user)
            if form.is_valid():
                form.save()
                return redirect("my_tasks", pk=request.user.id)
    else:
        return redirect("my_tasks", pk=request.user.id)
    return render(request, "tasks/new_task.html", {"page": page, "form": form})


@login_required(login_url="login")
def deleteTaskPage(request, pk):
    """View for deleting a task."""

    task = get_object_or_404(Task, pk=pk)
    object = task.title
    if task.project.owner == request.user:
        if request.method == "POST":
            task.delete()
            return redirect("my_tasks", pk=request.user.id)
    return render(request, "delete.html", {"task": task, "object": object})


@login_required(login_url="login")
def addMembers(request, pk):
    page = "edit"
    task = Task.objects.select_related("project").get(id=pk)
    if task.project.owner == request.user:
        form = TaskAddPartiicipantsForm(instance=task)

        if request.method == "POST":
            form = TaskAddPartiicipantsForm(request.POST, instance=task)
            if form.is_valid():
                form.save()
                return redirect("task_detail", pk=pk)
        return render(
            request, "tasks/create_update_task.html", {"form": form, "page": page}
        )

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q

from .models import Task, TaskFile, Comment
from projects.models import Project
from .forms import (
    TaskCreateForm,
    TaskAddPartiicipantsForm,
    CommentForm,
    TaskCreateFromProjectForm,
)


User = get_user_model()


@login_required(login_url="login")
def myTasksPage(request):
    """View for the page where current tasks of the user are depicted."""

    user = request.user
    tasks_all = (
        Task.objects.select_related("project", "project__owner", "assigned_to")
        .filter(Q(project__owner__id=user.id) | Q(assigned_to__id=user.id))
        .exclude(status="Completed")
        .only(
            "title",
            "uuid",
            "project__uuid",
            "project__name",
            "project__owner",
            "status",
            "priority",
            "deadline",
            "assigned_to__uuid",
            "assigned_to__name",
        )
    )

    tasks_assigned = tasks_all.filter(project__owner=user)
    tasks = tasks_all.filter(assigned_to=user)
    context = {"tasks": tasks, "tasks_assigned": tasks_assigned}
    return render(request, "tasks/my_tasks.html", context)


@login_required(login_url="login")
def taskDetailPage(request, pk):
    """View for detailed info of a task page."""

    user = request.user
    statuses = ["Awaits", "In Progress", "Completed"]

    comments = (
        Comment.objects.select_related("task", "task__project", "author")
        .filter(task__uuid=pk)
        .all()
    )

    if comments:
        task = comments.first().task
    else:
        task = Task.objects.select_related("assigned_to").get(uuid=pk)

    task.is_outdated()
    form = CommentForm()
    if request.user == task.project.owner or task.assigned_to == request.user:
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
def task_change_status(request, pk):
    """View for the form which changes the status of a task."""

    task = get_object_or_404(Task, uuid=pk)
    if request.method == "POST":
        new_status = request.POST["status"]
        task.status = new_status
        task.save()
        return redirect("task_detail", pk=pk)
    return HttpResponse("{'status': 200}")


@login_required(login_url="login")
def taskCreatePage(request):
    """View for creating a task page."""

    page = "create"
    user = request.user
    form = TaskCreateForm(user=user)

    if request.method == "POST":
        form = TaskCreateForm(request.POST, request.FILES, user=user)
        if form.is_valid():
            files = request.FILES.getlist("files")
            task = form.save(commit=True)

            for file in files:
                TaskFile.objects.create(task=task, file=file)

            return redirect("my_tasks")
    return render(
        request, "tasks/new_task.html", {"form": form, "page": page, "user": user}
    )


@login_required(login_url="login")
def create_task_from_project(request, pk):
    """View for creating a task from the project form."""

    page = "create"
    project = Project.objects.get(uuid=pk)

    form = TaskCreateFromProjectForm(project=project)
    if request.method == "POST":
        form = TaskCreateFromProjectForm(request.POST, request.FILES, project=project)

        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect("my_projects")
    return render(request, "tasks/new_task.html", {"form": form, "page": page})


@login_required(login_url="login")
def edit_task(request, pk):
    """View for editting the tasks form."""

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
    """View for deleting a task page."""

    task = get_object_or_404(Task, uuid=pk)
    object = task.title
    if task.project.owner == request.user:
        if request.method == "POST":
            task.delete()
            return redirect("my_tasks")
    return render(request, "delete.html", {"task": task, "object": object})


@login_required(login_url="login")
def change_assignee(request, pk):
    """View for changing an assignee for a task form."""

    page = "edit"
    task = Task.objects.select_related("project").get(uuid=pk)
    if task.project.owner == request.user:
        form = TaskAddPartiicipantsForm(instance=task)

        if request.method == "POST":
            form = TaskAddPartiicipantsForm(request.POST, instance=task)
            if form.is_valid():
                form.save()
                return redirect("task_detail", pk=pk)
        return render(request, "tasks/new_task.html", {"form": form, "page": page})

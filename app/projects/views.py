from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django.http import HttpResponse

from tasks.models import Task
from projects.models import Project, ProjectFile
from .forms import (
    ProjectCreationForm,
    ProjectAddParticipantsForm,
)


User = get_user_model()


@login_required(login_url="login")
def myProjectsPage(request):
    user = request.user

    projects_owned = Project.objects.filter(owner=user).distinct()

    projects_participated = (
        Task.objects.filter(assigned_to=user)
        .values("project__title", "project__uuid")
        .annotate(count=Count("project"))
    )

    context = {
        "projects_owned": projects_owned,
        "projects_participated": projects_participated,
    }
    return render(request, "projects/project_list.html", context)


@login_required(login_url="login")
def projectDetailPage(request, pk):
    project = get_object_or_404(
        Project.objects.prefetch_related(
            "tasks",
            "tasks__assigned_to",
            "project_files",
            "participants",
        ).select_related("owner"),
        uuid=pk,
    )
    # tasks = Task.objects.select_related(
    #     "project", "assigned_to", "project__owner"
    # ).filter(project__uuid=pk)
    # if tasks:
    #     project = tasks.first().project
    # else:
    #     project = get_object_or_404(Project, uuid=pk)

    attachments = project.project_files.all()
    participants = project.participants.all()

    context = {
        "project": project,
        "tasks": project.tasks.all(),
        "participants": participants,
        "attachments": attachments,
    }
    return render(request, "projects/project1.html", context)


@login_required(login_url="login")
def createProjectPage(request):
    page = "create"
    form = ProjectCreationForm()
    if request.method == "POST":
        form = ProjectCreationForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            files = request.FILES.getlist("files")
            project.save()

            for file in files:
                ProjectFile.objects.create(project=project, file=file)

            return redirect("my_projects")
    return render(request, "projects/project_create.html", {"form": form, "page": page})


@login_required(login_url="login")
def editProjectPage(request, pk):
    page = "edit"
    project = get_object_or_404(Project.objects.select_related("owner"), uuid=pk)
    if project.owner.id == request.user.id:
        form = ProjectCreationForm(instance=project)
        if request.method == "POST":
            form = ProjectCreationForm(request.POST, instance=project)
            if form.is_valid():
                files = request.FILES.getlist("files")
                form.save(commit=True)

                for file in files:
                    ProjectFile.objects.create(project=project, file=file)
                # form.save_m2m()
                return redirect("project", pk=pk)
    else:
        return redirect("my_tasks")
    return render(request, "projects/project_create.html", {"page": page, "form": form})


@login_required(login_url="login")
def deleteProjectPage(request, pk):
    project = get_object_or_404(Project.objects.select_related("owner"), uuid=pk)
    object = project.title
    if request.user.id == project.owner.id:
        if request.method == "POST":
            project.delete()
            return redirect("my_projects")
    else:
        return redirect("my_tasks")
    return render(request, "delete.html", {"project": project, "object": object})


@login_required(login_url="login")
def addMembers(request, pk):
    page = "add"
    project = get_object_or_404(Project.objects.select_related("owner"), uuid=pk)
    teammates = request.user.teammates.all()
    if project.owner == request.user:
        form = ProjectAddParticipantsForm(teammates=teammates, instance=project)

        if request.method == "POST":
            form = ProjectAddParticipantsForm(
                request.POST, teammates=teammates, instance=project
            )
            if form.is_valid():
                form.save()
                return redirect("project", pk=pk)
        return render(
            request,
            "projects/project_create.html",
            {"form": form, "page": page, "teammates": teammates},
        )


@login_required(login_url="login")
def removeMember(request, project_uuid, user_uuid):
    """View for removing a participant from the project."""

    project = get_object_or_404(Project, uuid=project_uuid)
    user = get_object_or_404(User, uuid=user_uuid)

    if request.user == project.owner:
        if request.method == "POST":
            tasks = Task.objects.filter(Q(project=project) & Q(assigned_to=user))
            for task in tasks:
                task.assigned_to = project.owner
                task.save()
            project.participants.remove(user)
            return redirect("project", pk=project_uuid)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Count, Subquery, OuterRef

from core.models import Project, Task
from .forms import ProjectCreationForm, ProjectAddParticipantsForm


@login_required(login_url="login")
def myProjectsPage(request, pk):
    user = get_object_or_404(get_user_model(), pk=pk)
    projects_owned = Project.objects.filter(owner=user)
    # projects_participated = Project.objects.filter(participants=user.id).annotate(
    #     tasks_count=Task.objects.filter(assigned_to=user)
    #     .values("project__id")
    #     .annotate(count=Count("project"))
    #     .values_list("count")
    # )

    projects_participated = (
        Task.objects.filter(assigned_to=user)
        .values("project__name", "project__id")
        .annotate(count=Count("project"))
    )

    # projects_participated = tasks_assigned.values_list("project", flat=True).annotate(
    #     count=Count("project")
    # )
    context = {
        "projects_owned": projects_owned,
        "projects_participated": projects_participated,
    }
    return render(request, "projects/project_list.html", context)


def projectPage(request, pk):
    project = get_object_or_404(Project, pk=pk)

    tasks = Task.objects.filter(project__id=pk)
    context = {
        "project": project,
        "tasks": tasks,
    }
    return render(request, "projects/project1.html", context)


@login_required(login_url="login")
def createProjectPage(request):
    page = "create"
    form = ProjectCreationForm()
    if request.method == "POST":
        form = ProjectCreationForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()

            return redirect("my_projects", pk=request.user.id)
    return render(request, "projects/project_create.html", {"form": form, "page": page})


@login_required(login_url="login")
def editProjectPage(request, pk):
    page = "edit"
    project = get_object_or_404(Project, pk=pk)
    if project.owner.id == request.user.id:
        form = ProjectCreationForm(instance=project)
        if request.method == "POST":
            form = ProjectCreationForm(request.POST, instance=project)
            if form.is_valid():
                form.save(commit=True)
                # form.save_m2m()
                return redirect("project", pk=pk)
    else:
        return redirect("home")
    return render(request, "projects/project_create.html", {"page": page, "form": form})


@login_required(login_url="login")
def deleteProjectPage(request, pk):
    project = get_object_or_404(Project, pk=pk)
    object = project.name
    if request.user.id == project.owner.id:
        if request.method == "POST":
            project.delete()
            return redirect("my_projects", pk=request.user.id)
    else:
        return redirect("home")
    return render(request, "delete.html", {"project": project, "object": object})


@login_required(login_url="login")
def addMembers(request, pk):
    page = "add"
    project = get_object_or_404(Project, pk=pk)
    if project.owner == request.user:
        form = ProjectAddParticipantsForm(instance=project)

        if request.method == "POST":
            form = ProjectAddParticipantsForm(request.POST, instance=project)
            if form.is_valid():
                form.save()
                return redirect("project", pk=pk)
        return render(
            request, "projects/project_create.html", {"form": form, "page": page}
        )

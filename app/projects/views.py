from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from core.models import Project, Task
from .forms import ProjectCreationForm


@login_required(login_url='login')
def myProjectsPage(request, pk):
    user = get_user_model().objects.get(id=pk)
    projects = Project.objects.filter(participants__id=user.id)
    return render(request, 'projects/my_projects.html', {'projects': projects})


def projectPage(request, pk):
    project = Project.objects.get(id=pk)
    tasks = Task.objects.filter(project__id=project.id)
    return render(request, 'projects/project.html', {'project': project, 'tasks': tasks})


@login_required(login_url='login')
def createProjectPage(request):
    page = 'create'
    form = ProjectCreationForm()
    if request.method == 'POST':
        form = ProjectCreationForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            form.save_m2m()
            return redirect('my_projects', pk=request.user.id)
    return render(request, 'projects/create_update_project.html', {'form': form, 'page': page})


@login_required(login_url='login')
def editProjectPage(request, pk):
    page = 'edit'
    project = Project.objects.get(id=pk)
    if project.owner.id == request.user.id:
        form = ProjectCreationForm(instance=project)
        if request.method == 'POST':
            form = ProjectCreationForm(request.POST, instance=project)
            if form.is_valid():
                form.save(commit=True)
                # form.save_m2m()
                return redirect('my_projects', pk=request.user.id)
    else:
        return redirect('home')
    return render(request, 'projects/create_update_project.html', {'page': page, 'form': form})


@login_required(login_url='login')
def deleteProjectPage(request, pk):
    project = Project.objects.get(id=pk)
    if request.user.id == project.owner.id:
        if request.method == 'POST':
            project.delete()
            return redirect('my_projects', pk=request.user.id)
    else:
        return redirect('home')
    return render(request, 'projects/delete_project.html', {'project': project})


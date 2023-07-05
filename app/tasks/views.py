from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from core.models import Task
from .forms import TaskCreateForm


@login_required(login_url='login')
def myTasksPage(request, pk):
    if not request.user:
        return redirect('home')
    user = get_user_model().objects.get(id=pk)
    tasks = Task.objects.filter(assigned_to=user)
    return render(request, 'tasks/my_tasks.html', {'tasks': tasks})


@login_required(login_url='login')
def taskDetailPage(request, pk):
    task = Task.objects.get(id=pk)
    assigned_to = task.assigned_to.all()
    return render(request, 'tasks/task_detail.html', {'task': task, 'assigned_to': assigned_to})


@login_required(login_url='login')
def taskCreatePage(request):
    """View for creating a task."""
    page = 'create'
    form = TaskCreateForm()
    if request.method == 'POST':
        form = TaskCreateForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('my_tasks', pk=request.user.id)
    return render(request, 'tasks/create_update_task.html', {'form': form, 'page': page})


@login_required(login_url='login')
def taskEditPage(request, pk):
    """View for editting the tasks."""
    page = 'edit'
    task = Task.objects.get(id=pk)
    if request.user.id == task.project.owner.id:
        form = TaskCreateForm(instance=task)
        if request.method == 'POST':
            form = TaskCreateForm(request.POST, instance=task)
            if form.is_valid():
                form.save()
                return redirect('my_tasks', pk=request.user.id)
    return render(request, 'tasks/create_update_task.html', {'page': page, 'form': form})


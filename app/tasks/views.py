from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from core.models import Task, Project, Comment
from .forms import TaskCreateForm, TaskAddPartiicipantsForm, CommentForm


@login_required(login_url='login')
def myTasksPage(request, pk):
    if not request.user:
        return redirect('home')
    user = get_user_model().objects.get(id=pk)
    
    tasks_assigned = Task.objects.filter(project__owner=user)
    tasks = Task.objects.filter(assigned_to=user)
    teammates = user.teammates.all()
    context = {
               'tasks': tasks, 'tasks_assigned': tasks_assigned, 'teammates': teammates}
    return render(request, 'tasks/start_page.html', context)


@login_required(login_url='login')
def taskDetailPage(request, pk):
    task = Task.objects.get(id=pk)
    task.is_outdated()
    assigned_to = task.assigned_to.all()
    comments = Comment.objects.filter(task=task)
    form = CommentForm()
    if request.user == task.project.owner or request.user in assigned_to:

        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
                comment.task = task
                comment.save()
                return redirect('task_detail', pk=pk)
    context = {'task': task, 'assigned_to': assigned_to, 'comments': comments, 'form': form}
    return render(request, 'tasks/task_detail.html', context)


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
    else:
        return redirect('my_tasks', pk=request.user.id)
    return render(request, 'tasks/create_update_task.html', {'page': page, 'form': form})


@login_required(login_url='login')
def deleteTaskPage(request, pk):
    """View for deleting a task."""
    task = Task.objects.get(id=pk)
    if task.project.owner == request.user:
        if request.method == 'POST':
            task.delete()
            return redirect('my_tasks', pk=request.user.id)
    return render(request, 'tasks/delete_task.html', {'task': task})


@login_required(login_url='login')
def addMembers(request, pk):
    page = 'edit'
    task = Task.objects.get(id=pk)
    if task.project.owner == request.user:
        form = TaskAddPartiicipantsForm(instance=task)

        if request.method == 'POST':
            form = TaskAddPartiicipantsForm(request.POST, instance=task)
            if form.is_valid():
                form.save()
                return redirect('task_detail', pk=pk)
        return render(request, 'tasks/create_update_task.html', {'form': form, 'page': page})

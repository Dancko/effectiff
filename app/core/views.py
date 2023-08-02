from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.db.models import Q

from .models import User, Project, Task


def home(request):
    q = request.GET.get('q')
    if q is not None:
        users = User.objects.filter(Q(email__icontains=q) | Q(name__icontains=q)).distinct()
        projects = Project.objects.filter(Q(participants=request.user.id) | Q(owner=request.user))
        projects_filtered = projects.filter(Q(name__icontains=q) | Q(description__icontains=q) |
                                            Q(category__name__icontains=q)).distinct()
        tasks = Task.objects.filter(Q(project__owner=request.user) | Q(assigned_to=request.user))
        tasks_filtered = tasks.filter(Q(title__icontains=q) |
                                      Q(body__icontains=q) |
                                      Q(category__name__icontains=q))
        context = {'users': users, 'projects_filtered': projects_filtered, 'q': q, 'tasks': tasks_filtered}
        return render(request, 'core/home.html', context)
    if request.user.is_authenticated:
        return redirect('my_tasks', pk=request.user.id)
    else:
        return render(request, 'core/home.html')

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from core.models import Project


@login_required(login_url='login')
def myProjectsPage(request, pk):
    user = get_user_model().objects.get(id=pk)
    projects = Project.objects.filter(participants__id=user.id)
    return render(request, 'projects/my_projects.html', {'projects': projects})

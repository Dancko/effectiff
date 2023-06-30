from django.shortcuts import render, redirect


def home(request):
    if request.user.is_authenticated:
        return redirect('my_tasks', pk=request.user.id)
    else:
        return render(request, 'core/home.html')

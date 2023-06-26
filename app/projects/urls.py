from django.urls import path

from . import views


urlpatterns = [
    path('my_projects/<int:pk>/', views.myProjectsPage, name='my_projects'),
    path('<int:pk>/', views.projectPage, name='project'),
    path('new_project/', views.createProjectPage, name='create_project'),
]
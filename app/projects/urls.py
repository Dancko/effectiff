from django.urls import path

from . import views


urlpatterns = [
    path('my_projects/<int:pk>/', views.myProjectsPage, name='my_projects'),
]
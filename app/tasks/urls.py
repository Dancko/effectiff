from django.urls import path

from . import views


urlpatterns = [
    path('my_tasks/<int:pk>/', views.myTasksPage, name='my_tasks'),
    path('<int:pk>/', views.taskDetailPage, name='task_detail'),
    path('create/', views.taskCreatePage, name='create_task'),
    path('edit/<int:pk>/', views.taskEditPage, name='edit_task'),
    path('delete/<int:pk>/', views.deleteTaskPage, name='delete_task'),

]
from django.urls import path

from . import views


urlpatterns = [
    path('my_tasks/<int:pk>/', views.myTasksPage, name='my_tasks'),

]
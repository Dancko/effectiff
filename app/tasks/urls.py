from django.urls import path

from . import views


urlpatterns = [
    path("", views.myTasksPage, name="my_tasks"),
    path("task/<uuid:pk>/", views.taskDetailPage, name="task_detail"),
    path("task/create/", views.taskCreatePage, name="create_task"),
    path(
        "task/create/project/<uuid:pk>/",
        views.taskCreateFromProject,
        name="create_task_from_project",
    ),
    path("task/edit/<uuid:pk>/", views.taskEditPage, name="edit_task"),
    path("task/delete/<uuid:pk>/", views.deleteTaskPage, name="delete_task"),
    path("task/add_members/<uuid:pk>/", views.addMembers, name="add_assignee"),
    path("task/change_st/<uuid:pk>/", views.taskChangeStatus, name="change_st"),
]

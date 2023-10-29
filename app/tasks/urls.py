from django.urls import path

from . import views


urlpatterns = [
    path("my_tasks/", views.myTasksPage, name="my_tasks"),
    path("<uuid:pk>/", views.taskDetailPage, name="task_detail"),
    path("create/", views.taskCreatePage, name="create_task"),
    path(
        "create/project/<uuid:pk>/",
        views.taskCreateFromProject,
        name="create_task_from_project",
    ),
    path("edit/<uuid:pk>/", views.taskEditPage, name="edit_task"),
    path("delete/<uuid:pk>/", views.deleteTaskPage, name="delete_task"),
    path("add_members/<uuid:pk>/", views.addMembers, name="add_assignee"),
    path("change_st/<uuid:pk>/", views.taskChangeStatus, name="change_st"),
]

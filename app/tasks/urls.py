from django.urls import path

from . import views


urlpatterns = [
    path("my_tasks/<str:pk>/", views.myTasksPage, name="my_tasks"),
    path("<str:pk>/", views.taskDetailPage, name="task_detail"),
    path("create/", views.taskCreatePage, name="create_task"),
    path(
        "create/project/<str:pk>/",
        views.taskCreateFromProject,
        name="create_task_from_project",
    ),
    path("edit/<str:pk>/", views.taskEditPage, name="edit_task"),
    path("delete/<str:pk>/", views.deleteTaskPage, name="delete_task"),
    path("add_assignee/<str:pk>/", views.addMembers, name="add_assignee"),
    path("change_st/<str:pk>/", views.taskChangeStatus, name="change_st"),
]

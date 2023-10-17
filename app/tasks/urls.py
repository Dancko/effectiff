from django.urls import path

from . import views


urlpatterns = [
    path("my_tasks/<int:pk>/", views.myTasksPage, name="my_tasks"),
    path("<int:pk>/", views.taskDetailPage, name="task_detail"),
    path("create/", views.taskCreatePage, name="create_task"),
    path(
        "create/project/<int:pk>/",
        views.taskCreateFromProject,
        name="create_task_from_project",
    ),
    path("edit/<int:pk>/", views.taskEditPage, name="edit_task"),
    path("delete/<int:pk>/", views.deleteTaskPage, name="delete_task"),
    path("add_assignee/<int:pk>/", views.addMembers, name="add_assignee"),
    path("change_st/<int:pk>/", views.taskChangeStatus, name="change_st"),
]

from django.urls import path

from . import views


urlpatterns = [
    path("my_projects/<str:pk>/", views.myProjectsPage, name="my_projects"),
    path("<str:pk>/", views.projectPage, name="project"),
    path("new_project/", views.createProjectPage, name="create_project"),
    path("edit_project/<str:pk>/", views.editProjectPage, name="edit_project"),
    path("delete/<str:pk>/", views.deleteProjectPage, name="delete_project"),
    path("add/<str:pk>/", views.addMembers, name="add_members"),
]

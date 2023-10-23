from django.urls import path

from . import views


urlpatterns = [
    path("my_projects/<uuid:pk>/", views.myProjectsPage, name="my_projects"),
    path("<uuid:pk>/", views.projectPage, name="project"),
    path("new_project/", views.createProjectPage, name="create_project"),
    path("edit_project/<uuid:pk>/", views.editProjectPage, name="edit_project"),
    path("delete/<uuid:pk>/", views.deleteProjectPage, name="delete_project"),
    path("add/<uuid:pk>/", views.addMembers, name="add_members"),
]

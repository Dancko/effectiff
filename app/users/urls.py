from django.urls import path

from users import views


urlpatterns = [
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutPage, name="logout"),
    path("register/", views.registerPage, name="register"),
    path("<str:pk>/", views.profilePage, name="profile"),
    path("edit/<str:pk>/", views.editProfilePage, name="edit_profile"),
    path("delete/<str:pk>/", views.deleteProfile, name="delete_profile"),
]

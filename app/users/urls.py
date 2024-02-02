from django.urls import path

from users import views


urlpatterns = [
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutPage, name="logout"),
    path("register/", views.registerPage, name="register"),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
    path(
        "password_reset/<uidb64>/<token>/",
        views.password_reset_activate,
        name="password_reset_activate",
    ),
    path("password_reset/", views.password_reset, name="password_reset"),
    path(
        "password_reset_sent/",
        views.password_reset_message_sent,
        name="password_reset_sent",
    ),
    path("verification_sent/", views.verification_sent, name="verification_sent"),
    path("<uuid:pk>/", views.profilePage, name="profile"),
    path("edit/<uuid:pk>/", views.editProfilePage, name="edit_profile"),
    path("my_team/", views.myTeamPage, name="my_team"),
    # path("delete/<uuid:pk>/", views.deleteProfilePage, name="delete_profile"),
    path("add_teammate/<uuid:pk>/", views.add_to_team, name="add_teammate"),
    path("delete_teammate/<uuid:pk>/", views.delete_from_team, name="delete_teammate"),
    path("change_password/", views.setPasswordPage, name="change_password"),
]

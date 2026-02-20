from django.urls import path
from . import views



urlpatterns = [
    path("", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),

    path("user/", views.user_dashboard, name="user_dashboard"),
    path("manager/", views.manager_dashboard, name="manager_dashboard"),
     path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),

    path("add-note/", views.add_note, name="add_note"),
    path("request-delete/<int:note_id>/", views.request_delete, name="request_delete"),

    path("approve/<int:note_id>/", views.approve_note, name="approve_note"),
    path("reject/<int:note_id>/", views.reject_note, name="reject_note"),

    path("admin-delete/<int:note_id>/", views.admin_delete, name="admin_delete"),
    path("logout/", views.logout_view, name="logout"),

]
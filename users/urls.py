from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),  # Have the root route render a page where users can register or log in
    path("success/", views.success),
    path("register/", views.register_user),
    path("login/", views.login_user),
    path("logout/", views.logout_user),
]

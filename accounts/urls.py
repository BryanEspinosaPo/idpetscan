from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("registro/", views.register_view, name="register"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
]
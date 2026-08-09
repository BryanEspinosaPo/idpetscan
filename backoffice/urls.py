from django.urls import path

from . import views

app_name = "backoffice"

urlpatterns = [
    path("login/", views.AdminLoginView.as_view(), name="login"),
    path("solicitudes/", views.solicitudes_view, name="solicitudes"),
    path("solicitudes/<int:pk>/aprobar/", views.approve_pet_view, name="approve_pet"),
    path("solicitudes/<int:pk>/rechazar/", views.reject_pet_view, name="reject_pet"),
    path("mascotas/", views.mascotas_view, name="mascotas"),
    path("usuarios/", views.usuarios_view, name="usuarios"),
    path("ordenes/", views.ordenes_view, name="ordenes"),
]

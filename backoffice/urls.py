from django.urls import path

from . import views

app_name = "backoffice"

urlpatterns = [
    path("login/", views.AdminLoginView.as_view(), name="login"),
    path("solicitudes/", views.solicitudes_view, name="solicitudes"),
    path("solicitudes/<int:pk>/aprobar/", views.approve_pet_view, name="approve_pet"),
    path("solicitudes/<int:pk>/rechazar/", views.reject_pet_view, name="reject_pet"),
    path("mascotas/", views.mascotas_view, name="mascotas"),
    path("mascotas/<int:pk>/historia-clinica/", views.toggle_medical_history_view, name="toggle_medical_history"),
    path("mascotas/<int:pk>/renovar/", views.renew_subscription_view, name="renew_subscription"),
    path("usuarios/", views.usuarios_view, name="usuarios"),
    path("ordenes/", views.ordenes_view, name="ordenes"),
    path("ordenes/<int:pk>/actualizar/", views.update_order_view, name="update_order"),
    path("ordenes/<int:pk>/marcar-pagada/", views.mark_order_paid_view, name="mark_order_paid"),
]

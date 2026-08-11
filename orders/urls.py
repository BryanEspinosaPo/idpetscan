from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    path("planes/", views.plans_view, name="plans"),
    path("crear/<str:plan>/", views.create_order_view, name="create_order"),
    path("<int:order_id>/pagar/", views.checkout_view, name="checkout"),
    path("<int:order_id>/confirmacion/", views.confirmation_view, name="confirmation"),
]
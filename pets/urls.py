from django.urls import path

from . import views

app_name = "pets"

urlpatterns = [
    path("mis-mascotas/", views.my_pets_view, name="my_pets"),
    path("mis-mascotas/nueva/", views.create_pet_view, name="create_pet"),
    path("mis-mascotas/<int:pk>/editar/", views.edit_pet_view, name="edit_pet"),
    path("registro-exitoso/<str:public_code>/", views.pet_created_view, name="pet_created"),
    path("p/<str:public_code>/", views.public_profile_view, name="public_profile"),
]
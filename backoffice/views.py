from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST


from orders.models import Order
from pets.emails import send_admin_notification, send_owner_status_email
from pets.models import Pet
from pets.utils import generate_qr_for_pet


def is_staff(user):
    return user.is_authenticated and user.is_staff


class AdminLoginView(LoginView):
    template_name = "backoffice/login.html"

    def get_success_url(self):
        return "/panel/solicitudes/"


@user_passes_test(is_staff, login_url="backoffice:login")
def solicitudes_view(request):
    pending = Pet.objects.filter(status="pending").order_by("-created_at")
    return render(request, "backoffice/solicitudes.html", {"pending": pending, "active": "solicitudes"})


@user_passes_test(is_staff, login_url="backoffice:login")
@require_POST
def approve_pet_view(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    if not pet.qr_code:
        generate_qr_for_pet(pet)
    pet.status = "approved"
    pet.approved_at = timezone.now()
    pet.save()
    send_admin_notification(pet)
    send_owner_status_email(pet)
    return redirect("backoffice:solicitudes")


@user_passes_test(is_staff, login_url="backoffice:login")
@require_POST
def reject_pet_view(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    pet.status = "rejected"
    pet.save()
    send_owner_status_email(pet)
    return redirect("backoffice:solicitudes")


@user_passes_test(is_staff, login_url="backoffice:login")
def mascotas_view(request):
    pets = Pet.objects.all().order_by("-created_at")
    return render(request, "backoffice/mascotas.html", {"pets": pets, "active": "mascotas"})


@user_passes_test(is_staff, login_url="backoffice:login")
def usuarios_view(request):
    users = User.objects.annotate(pet_count=Count("pets")).order_by("-date_joined")
    return render(request, "backoffice/usuarios.html", {"users": users, "active": "usuarios"})


@user_passes_test(is_staff, login_url="backoffice:login")
def ordenes_view(request):
    orders = Order.objects.all().order_by("-created_at")
    return render(request, "backoffice/ordenes.html", {"orders": orders, "active": "ordenes"})

@user_passes_test(is_staff, login_url="backoffice:login")
@require_POST
def mark_order_paid_view(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.payment_status = "paid"
    order.save()
    return redirect("backoffice:ordenes")

@user_passes_test(is_staff, login_url="backoffice:login")
@require_POST
def toggle_medical_history_view(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    pet.clinical_history_enabled = not pet.clinical_history_enabled
    pet.save()
    return redirect("backoffice:mascotas")
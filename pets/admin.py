from django.contrib import admin
from django.utils import timezone

from .emails import send_admin_notification, send_owner_status_email
from .models import Pet
from .utils import generate_qr_for_pet


@admin.action(description="Aprobar mascotas seleccionadas")
def approve_pets(modeladmin, request, queryset):
    for pet in queryset:
        if not pet.qr_code:
            generate_qr_for_pet(pet)
        pet.status = "approved"
        pet.approved_at = timezone.now()
        pet.save()
        send_admin_notification(pet)
        send_owner_status_email(pet)


@admin.action(description="Rechazar mascotas seleccionadas")
def reject_pets(modeladmin, request, queryset):
    for pet in queryset:
        pet.status = "rejected"
        pet.save()
        send_owner_status_email(pet)


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ("name", "species", "owner", "status", "is_lost", "created_at")
    list_filter = ("status", "species", "is_lost")
    search_fields = ("name", "owner__username", "contact_phone", "public_code")
    readonly_fields = ("public_code", "qr_code", "created_at", "updated_at", "approved_at")
    actions = [approve_pets, reject_pets]
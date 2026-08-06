from django.contrib import admin

from .models import Pet


@admin.action(description="Aprobar mascotas seleccionadas")
def approve_pets(modeladmin, request, queryset):
    from django.utils import timezone

    queryset.update(status="approved", approved_at=timezone.now())


@admin.action(description="Rechazar mascotas seleccionadas")
def reject_pets(modeladmin, request, queryset):
    queryset.update(status="rejected")


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ("name", "species", "owner", "status", "is_lost", "created_at")
    list_filter = ("status", "species", "is_lost")
    search_fields = ("name", "owner__username", "contact_phone", "public_code")
    readonly_fields = ("public_code", "created_at", "updated_at", "approved_at")
    actions = [approve_pets, reject_pets]
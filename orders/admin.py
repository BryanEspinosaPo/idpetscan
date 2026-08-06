from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "plan", "amount", "payment_status", "production_status", "created_at")
    list_filter = ("payment_status", "production_status", "plan")
    search_fields = ("user__username", "payment_reference")
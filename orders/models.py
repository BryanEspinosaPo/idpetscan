import secrets

from django.conf import settings
from django.db import models


def generate_order_reference():
    return f"idpetscan-{secrets.token_hex(8)}"


class Order(models.Model):
    PLAN_CHOICES = [
        ("classic", "Clásica"),
        ("family", "Familiar"),
        ("premium", "Premium"),
    ]

    PAYMENT_STATUS_CHOICES = [
        ("pending", "Pendiente"),
        ("paid", "Pagado"),
        ("failed", "Fallido"),
    ]

    PRODUCTION_STATUS_CHOICES = [
        ("waiting", "En espera"),
        ("in_production", "En producción"),
        ("shipped", "Enviado"),
        ("delivered", "Entregado"),
    ]

    reference = models.CharField(max_length=64, unique=True, default=generate_order_reference, editable=False)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders"
    )
    pet = models.OneToOneField(
        "pets.Pet", on_delete=models.SET_NULL, null=True, blank=True, related_name="order"
    )

    plan = models.CharField(max_length=10, choices=PLAN_CHOICES, default="classic")
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    payment_status = models.CharField(
        max_length=10, choices=PAYMENT_STATUS_CHOICES, default="pending"
    )
    production_status = models.CharField(
        max_length=15, choices=PRODUCTION_STATUS_CHOICES, default="waiting"
    )

    payment_reference = models.CharField(max_length=100, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Orden #{self.pk} — {self.get_plan_display()} — {self.user}"

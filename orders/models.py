import secrets

from django.conf import settings
from django.db import models

PLAN_PRICES = {
    "classic": 50000,
    "premium": 85000,
    "family": 135000,
}

PLAN_PET_LIMITS = {
    "classic": 1,
    "premium": 1,
    "family": 2,
}

PLAN_MEDICAL_HISTORY = {
    "classic": False,
    "premium": True,
    "family": True,
}


def generate_order_reference():
    return f"idpetscan-{secrets.token_hex(8)}"


class Order(models.Model):
    PLAN_CHOICES = [
        ("classic", "Básico"),
        ("premium", "Premium"),
        ("family", "Familiar"),
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

    plan = models.CharField(max_length=10, choices=PLAN_CHOICES, default="classic")
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    payment_status = models.CharField(
        max_length=10, choices=PAYMENT_STATUS_CHOICES, default="pending"
    )
    production_status = models.CharField(
        max_length=15, choices=PRODUCTION_STATUS_CHOICES, default="waiting"
    )

    payment_reference = models.CharField(max_length=100, blank=True)

    shipping_address = models.CharField(max_length=255, blank=True, verbose_name="Dirección de envío")
    shipping_city = models.CharField(max_length=100, blank=True, verbose_name="Ciudad")
    tracking_number = models.CharField(max_length=100, blank=True, verbose_name="Número de guía")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Orden #{self.pk} — {self.get_plan_display()} — {self.user}"

    @property
    def pet_limit(self):
        return PLAN_PET_LIMITS.get(self.plan, 1)

    @property
    def pets_remaining(self):
        return max(0, self.pet_limit - self.pets.count())

    @property
    def includes_medical_history(self):
        return PLAN_MEDICAL_HISTORY.get(self.plan, False)

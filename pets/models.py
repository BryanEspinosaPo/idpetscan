
import secrets
import string

from django.conf import settings
from django.db import models


def generate_public_code():
    """
    Genera un código corto y aleatorio (no adivinable) que se usa
    en la URL pública del perfil y en el QR. No es el ID interno.
    """
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(8))


class Pet(models.Model):
    SPECIES_CHOICES = [
        ("dog", "Perro"),
        ("cat", "Gato"),
        ("other", "Otro"),
    ]

    SEX_CHOICES = [
        ("male", "Macho"),
        ("female", "Hembra"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pendiente de aprobación"),
        ("approved", "Aprobado / Publicado"),
        ("rejected", "Rechazado"),
    ]

    # --- Identificadores ---
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="pets"
    )
    public_code = models.CharField(
        max_length=8, unique=True, default=generate_public_code, editable=False
    )

    # --- Datos de la mascota ---
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=10, choices=SPECIES_CHOICES, default="dog")
    breed = models.CharField(max_length=100, blank=True)
    sex = models.CharField(max_length=6, choices=SEX_CHOICES, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    color = models.CharField(max_length=100, blank=True)
    size = models.CharField(max_length=50, blank=True)
    photo = models.ImageField(upload_to="pets/", blank=True, null=True)
    qr_code = models.ImageField(upload_to="qr_codes/", blank=True, null=True)

    # --- Contacto del dueño ---
    contact_name = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=20)
    contact_phone_alt = models.CharField(max_length=20, blank=True)
    contact_email = models.EmailField(blank=True)
    zone = models.CharField(max_length=100, blank=True)

    # --- Salud ---
    vaccines_ok = models.BooleanField(default=False)
    neutered = models.BooleanField(default=False)
    allergies = models.TextField(blank=True)
    medical_conditions = models.TextField(blank=True)
    vet_name = models.CharField(max_length=150, blank=True)
    vet_phone = models.CharField(max_length=20, blank=True)

    # --- Estado / "perdido" ---
    is_lost = models.BooleanField(default=False)
    last_seen_location = models.CharField(max_length=200, blank=True)
    last_seen_date = models.DateField(null=True, blank=True)
    reward = models.CharField(max_length=100, blank=True)

    # --- Flujo de aprobación ---
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    rejection_reason = models.TextField(blank=True)

    # --- Metadatos ---
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.get_species_display()})"
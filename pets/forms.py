from django import forms

from .models import Pet


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = [
            # Datos de la mascota
            "name", "species", "breed", "sex", "birth_date", "color", "size", "photo",
            # Contacto del dueño
            "contact_name", "contact_phone", "contact_phone_alt", "contact_email", "zone",
            # Salud
            "vaccines_ok", "neutered", "allergies", "medical_conditions",
            "vet_name", "vet_phone",
        ]
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}),
            "allergies": forms.Textarea(attrs={"rows": 3}),
            "medical_conditions": forms.Textarea(attrs={"rows": 3}),
        }
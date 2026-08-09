from django import forms

from .models import Pet


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = [
            "name", "species", "breed", "sex", "birth_date", "color", "size", "photo",
            "contact_name", "contact_phone", "contact_phone_alt", "contact_email", "zone",
            "vaccines_ok", "neutered", "allergies", "medical_conditions",
            "clinical_notes", "vet_name", "vet_phone",
        ]
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}),
            "allergies": forms.Textarea(attrs={"rows": 3}),
            "medical_conditions": forms.Textarea(attrs={"rows": 3}),
            "clinical_notes": forms.Textarea(attrs={"rows": 3}),
        }
        labels = {
            "name": "Nombre",
            "species": "Especie",
            "breed": "Raza",
            "sex": "Sexo",
            "birth_date": "Fecha de nacimiento",
            "color": "Color",
            "size": "Tamaño",
            "photo": "Foto",
            "contact_name": "Nombre del dueño",
            "contact_phone": "Teléfono principal",
            "contact_phone_alt": "Teléfono alternativo",
            "contact_email": "Correo electrónico",
            "zone": "Zona / barrio",
            "vaccines_ok": "Vacunas al día",
            "neutered": "Esterilizado",
            "allergies": "Alergias",
            "medical_conditions": "Condiciones médicas",
            "clinical_notes": "Novedades clínicas",
            "vet_name": "Nombre del veterinario",
            "vet_phone": "Teléfono del veterinario",
        }
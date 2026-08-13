from django import forms

from.models import MedicalRecord, Pet




class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = [
            "name", "species", "breed", "sex", "birth_date", "color", "size", "photo",
            "contact_name", "contact_phone", "contact_phone_alt", "contact_email", "zone",
            "vaccines_ok", "neutered", "allergies", "medical_conditions", "clinical_notes",
            "vet_name", "vet_phone",
            "is_lost", "last_seen_location", "last_seen_date", "reward",
        ]
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}),
            "allergies": forms.Textarea(attrs={"rows": 3}),
            "medical_conditions": forms.Textarea(attrs={"rows": 3}),
            "clinical_notes": forms.Textarea(attrs={"rows": 3}),
            "last_seen_date": forms.DateInput(attrs={"type": "date"}),
            "is_lost": forms.CheckboxInput(attrs={"id": "id_is_lost_toggle"}),
        }
        labels = {
            "name": "Nombre", "species": "Especie", "sex": "Sexo",
            "birth_date": "Fecha de nacimiento", "color": "Color", "size": "Tamaño", "photo": "Foto",
            "contact_name": "Nombre del dueño", "contact_phone": "Teléfono principal",
            "contact_phone_alt": "Teléfono alternativo", "contact_email": "Correo electrónico",
            "zone": "Zona / barrio",
            "vaccines_ok": "Vacunas al día", "neutered": "Esterilizado", "allergies": "Alergias",
            "medical_conditions": "Condiciones médicas", "clinical_notes": "Novedades clínicas",
            "vet_name": "Nombre del veterinario", "vet_phone": "Teléfono del veterinario",
            "is_lost": "Mi mascota está perdida",
            "last_seen_location": "Última zona vista",
            "last_seen_date": "Fecha en que se perdió",
            "reward": "Recompensa (opcional)",
        }

class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ["date", "description"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 2, "placeholder": "Ej: Vacuna antirrábica aplicada, control de peso, etc."}),
        }
        labels = {"date": "Fecha", "description": "Novedad"}
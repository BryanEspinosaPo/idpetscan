from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo electrónico")
    accepts_data_policy = forms.BooleanField(
        required=True,
        label="He leído y autorizo el tratamiento de mis datos personales según la Política de Tratamiento de Datos.",
        error_messages={"required": "Debes autorizar el tratamiento de datos para poder registrarte."},
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
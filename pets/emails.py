from django.conf import settings
from django.core.mail import EmailMessage


def send_admin_notification(pet):
    subject = f"Nueva placa aprobada: {pet.name}"
    plan_line = f"Plan: {pet.order.get_plan_display()}\n" if pet.order else ""
    body = (
        f"Mascota: {pet.name}\n"
        f"Especie: {pet.get_species_display()}\n"
        f"Dueño: {pet.contact_name}\n"
        f"Celular de contacto: {pet.contact_phone}\n"
        f"Código público: {pet.public_code}\n"
        f"{plan_line}"
        f"Historia clínica incluida: {'Sí' if pet.clinical_history_enabled else 'No'}\n"
    )

    email = EmailMessage(
        subject=subject,
        body=body,
        to=[settings.ADMIN_NOTIFICATION_EMAIL],
    )
    if pet.qr_code:
        email.attach_file(pet.qr_code.path)
    email.send(fail_silently=False)


def send_owner_status_email(pet):
    subject = f"¡{pet.name} ya está publicado en IDPetScan!"
    body = (
        f"Tu mascota {pet.name} ya está publicada.\n\n"
        f"Código de identificación público: {pet.public_code}\n"
        f"Perfil: https://idpetscan.com/p/{pet.public_code}/\n"
    )
    if pet.clinical_history_enabled:
        body += (
            f"\nTu plan incluye historia clínica digital.\n"
            f"Código de acceso al historial médico: {pet.medical_access_code}\n"
            f"Compártelo solo con quien deba consultarlo (veterinario, familiar, etc.).\n"
        )
    if pet.renewal_due_date:
        body += f"\nEl mantenimiento anual de este perfil vence el {pet.renewal_due_date.strftime('%d/%m/%Y')}.\n"

    if pet.contact_email:
        EmailMessage(subject=subject, body=body, to=[pet.contact_email]).send(fail_silently=True)

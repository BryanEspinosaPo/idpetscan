from django.conf import settings
from django.core.mail import EmailMessage


def send_admin_notification(pet):
    subject = f"Nueva placa aprobada: {pet.name}"
    plan_line = f"Plan: {pet.order.get_plan_display()}\n" if pet.order else ""
    qr_line = f"QR (descargar): {pet.qr_code.url}\n" if pet.qr_code else "QR: no generado\n"
    photo_line = f"Foto: {pet.photo.url}\n" if pet.photo else ""
    body = (
        f"Mascota: {pet.name}\n"
        f"Especie: {pet.get_species_display()}\n"
        f"Dueño: {pet.contact_name}\n"
        f"Celular de contacto: {pet.contact_phone}\n"
        f"Código público: {pet.public_code}\n"
        f"{plan_line}"
        f"Historia clínica incluida: {'Sí' if pet.clinical_history_enabled else 'No'}\n"
        f"{qr_line}"
        f"{photo_line}"
    )

    email = EmailMessage(
        subject=subject,
        body=body,
        to=[settings.PRODUCTION_NOTIFICATION_EMAIL],
    )
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


def send_renewal_reminder_email(pet):
    subject = f"Recuerda renovar el mantenimiento de {pet.name}"
    body = (
        f"Hola,\n\n"
        f"El mantenimiento anual del perfil de {pet.name} vence el "
        f"{pet.renewal_due_date.strftime('%d/%m/%Y')}.\n\n"
        f"El costo de la renovación es de $25.000. Escríbenos por WhatsApp para coordinar el pago "
        f"y evitar que el perfil público de {pet.name} se desactive.\n\n"
        f"Código de identificación: {pet.public_code}"
    )
    if pet.contact_email:
        EmailMessage(subject=subject, body=body, to=[pet.contact_email]).send(fail_silently=True)

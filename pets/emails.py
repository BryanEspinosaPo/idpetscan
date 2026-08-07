
from django.conf import settings
from django.core.mail import EmailMessage


def send_admin_notification(pet):
    """
    Le llega a ti (ADMIN_NOTIFICATION_EMAIL): nombre de la mascota,
    celular de contacto y el QR adjunto, listo para producción de la placa.
    """
    subject = f"Nueva placa aprobada: {pet.name}"
    body = (
        f"Mascota: {pet.name}\n"
        f"Especie: {pet.get_species_display()}\n"
        f"Dueño: {pet.contact_name}\n"
        f"Celular de contacto: {pet.contact_phone}\n"
        f"Código público: {pet.public_code}\n"
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
    """Le avisa al dueño si su mascota fue aprobada o rechazada."""
    if pet.status == "approved":
        subject = f"¡{pet.name} ya está publicado en IDPetScan!"
        body = f"Tu mascota {pet.name} fue aprobada. Ya puedes descargar y usar su QR."
    else:
        subject = f"Tu solicitud para {pet.name} fue rechazada"
        body = f"Motivo: {pet.rejection_reason or 'No especificado'}"

    if pet.contact_email:
        EmailMessage(subject=subject, body=body, to=[pet.contact_email]).send(fail_silently=True)
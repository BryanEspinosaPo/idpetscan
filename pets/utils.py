import io

import qrcode
from django.core.files.base import ContentFile


def generate_qr_for_pet(pet, base_url="http://127.0.0.1:8000"):
    """
    Genera el QR que apunta al perfil público de la mascota y lo
    guarda directamente en el campo qr_code del modelo.
    En producción, base_url debe ser "https://idpetscan.com".
    """
    public_url = f"{base_url}/p/{pet.public_code}/"

    qr = qrcode.QRCode(box_size=10, border=2)
    qr.add_data(public_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#0D1B2A", back_color="white")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")

    filename = f"qr_{pet.public_code}.png"
    pet.qr_code.save(filename, ContentFile(buffer.getvalue()), save=False)
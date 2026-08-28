import os

import cloudinary
import cloudinary.uploader
from django.core.files.storage import Storage


class CloudinaryMediaStorage(Storage):
    """
    Storage minimo para guardar fotos/QR en Cloudinary usando el SDK
    directo, sin depender de django-cloudinary-storage (que interfiere
    con collectstatic).
    """

    def _save(self, name, content):
        folder = os.path.dirname(name)
        base = os.path.splitext(os.path.basename(name))[0]
        public_id = f"{folder}/{base}" if folder else base

        result = cloudinary.uploader.upload(
            content,
            public_id=public_id,
            resource_type="image",
            overwrite=True,
            unique_filename=False,
        )
        ext = result.get("format", "")
        return f"{result['public_id']}.{ext}" if ext else result["public_id"]

    def _open(self, name, mode="rb"):
        raise NotImplementedError("Este storage no soporta lectura directa de archivos")

    def exists(self, name):
        return False

    def url(self, name):
        base, ext = os.path.splitext(name)
        ext = ext.lstrip(".")
        if ext:
            return cloudinary.CloudinaryImage(base).build_url(format=ext, secure=True)
        return cloudinary.CloudinaryImage(name).build_url(secure=True)

    def size(self, name):
        return 0

    def delete(self, name):
        base, _ = os.path.splitext(name)
        cloudinary.uploader.destroy(base)

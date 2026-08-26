from django.contrib.staticfiles.finders import get_finders
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.core.management.base import BaseCommand
import os


class Command(BaseCommand):
    help = "Copia archivos estaticos manualmente (workaround para bug de collectstatic)"

    def handle(self, *args, **options):
        os.makedirs(settings.STATIC_ROOT, exist_ok=True)
        target_storage = FileSystemStorage(location=settings.STATIC_ROOT)

        count = 0
        for finder in get_finders():
            for path, storage in finder.list([]):
                if target_storage.exists(path):
                    target_storage.delete(path)
                with storage.open(path) as source_file:
                    target_storage.save(path, source_file)
                count += 1

        self.stdout.write(self.style.SUCCESS(f"{count} archivos estaticos copiados correctamente"))

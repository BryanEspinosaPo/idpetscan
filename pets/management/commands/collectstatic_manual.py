import os
import shutil

from django.contrib.staticfiles.finders import get_finders
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Copia archivos estaticos manualmente (workaround para bug de collectstatic)"

    def handle(self, *args, **options):
        root = str(settings.STATIC_ROOT)
        os.makedirs(root, exist_ok=True)

        count = 0
        for finder in get_finders():
            for path, storage in finder.list([]):
                source_path = storage.path(path)
                dest_path = os.path.join(root, path)
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.copy2(source_path, dest_path)
                count += 1

        self.stdout.write(self.style.SUCCESS(f"{count} archivos estaticos copiados correctamente"))

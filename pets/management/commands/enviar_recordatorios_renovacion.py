from datetime import date, timedelta

from django.core.management.base import BaseCommand

from pets.emails import send_renewal_reminder_email
from pets.models import Pet


class Command(BaseCommand):
    help = "Envía recordatorio por email a mascotas cuyo mantenimiento vence en 15 días o menos."

    def handle(self, *args, **options):
        limite = date.today() + timedelta(days=15)
        pets = Pet.objects.filter(
            status="approved",
            subscription_active=True,
            renewal_due_date__lte=limite,
            renewal_due_date__gte=date.today(),
            renewal_reminder_sent=False,
        )

        count = 0
        for pet in pets:
            send_renewal_reminder_email(pet)
            pet.renewal_reminder_sent = True
            pet.save()
            count += 1
            self.stdout.write(f"Recordatorio enviado a {pet.name} ({pet.contact_email})")

        self.stdout.write(self.style.SUCCESS(f"Total de recordatorios enviados: {count}"))

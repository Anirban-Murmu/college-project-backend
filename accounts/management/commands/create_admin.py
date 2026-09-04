import os

from django.core.management.base import BaseCommand
from accounts.models import User


class Command(BaseCommand):
    help = "Create or update the production superuser."

    def handle(self, *args, **options):
        email = os.environ.get(
            "DJANGO_SUPERUSER_EMAIL",
            ""
        ).strip().lower()

        password = os.environ.get(
            "DJANGO_SUPERUSER_PASSWORD",
            ""
        )

        first_name = os.environ.get(
            "DJANGO_SUPERUSER_FIRST_NAME",
            "Admin"
        )

        last_name = os.environ.get(
            "DJANGO_SUPERUSER_LAST_NAME",
            "User"
        )

        gender = os.environ.get(
            "DJANGO_SUPERUSER_GENDER",
            "other"
        )

        tc = (
            os.environ.get(
                "DJANGO_SUPERUSER_TC",
                "True"
            ).lower() == "true"
        )

        if not email:
            self.stdout.write(
                self.style.ERROR(
                    "DJANGO_SUPERUSER_EMAIL is missing."
                )
            )
            return

        if not password:
            self.stdout.write(
                self.style.ERROR(
                    "DJANGO_SUPERUSER_PASSWORD is missing."
                )
            )
            return

        user, created = User.objects.get_or_create(
            email=email
        )

        user.first_name = first_name
        user.last_name = last_name
        user.gender = gender
        user.tc = tc
        user.is_active = True
        user.is_admin = True
        user.is_superuser = True

        # Django hashes the password
        user.set_password(password)

        user.save()

        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Superuser created: {email}"
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Superuser updated: {email}"
                )
            )
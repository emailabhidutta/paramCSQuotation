from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password

class Command(BaseCommand):
    help = 'Test password setting and checking'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)

    def handle(self, *args, **options):
        UserModel = get_user_model()
        username = options['username']
        password = options['password']

        try:
            user = UserModel.objects.get(Name=username)
            self.stdout.write(f"User found: {user}")
            self.stdout.write(f"Current password hash: {user.password}")

            # Test setting password
            user.set_password(password)
            self.stdout.write(f"New password hash after set_password: {user.password}")
            user.save()
            user.refresh_from_db()
            self.stdout.write(f"Password hash after save: {user.password}")

            # Test checking password
            if user.check_password(password):
                self.stdout.write(self.style.SUCCESS("Password check successful"))
            else:
                self.stdout.write(self.style.ERROR("Password check failed"))

            # Test with Django's check_password function
            if check_password(password, user.password):
                self.stdout.write(self.style.SUCCESS("Django's check_password successful"))
            else:
                self.stdout.write(self.style.ERROR("Django's check_password failed"))

        except UserModel.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"User with username {username} does not exist"))

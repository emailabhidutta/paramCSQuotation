from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password, make_password
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Verify user credentials'

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
            self.stdout.write(f"Is user active: {user.is_active}")
            self.stdout.write(f"Is user staff: {user.is_staff}")
            self.stdout.write(f"Is user superuser: {user.is_superuser}")
            self.stdout.write(f"Stored password hash: {user.password}")

            # Check using Django's check_password
            django_check = check_password(password, user.password)
            self.stdout.write(f"Django's check_password result: {django_check}")
            logger.debug(f"Django's check_password result: {django_check}")

            # Check using user's check_password method
            user_check = user.check_password(password)
            self.stdout.write(f"user.check_password result: {user_check}")
            logger.debug(f"user.check_password result: {user_check}")

            # Generate a new hash for comparison
            new_hash = make_password(password)
            self.stdout.write(f"Newly generated hash: {new_hash}")

            # Log the password being checked (be cautious with this in production)
            logger.debug(f"Password being checked: {password}")

            if django_check and user_check:
                self.stdout.write(self.style.SUCCESS("Password is correct"))
            else:
                self.stdout.write(self.style.ERROR("Password is incorrect"))

            # Additional debugging
            self.stdout.write(f"User model: {UserModel}")
            self.stdout.write(f"User object type: {type(user)}")
            self.stdout.write(f"User's check_password method: {user.check_password}")

        except UserModel.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"User with username {username} does not exist"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))
            logger.exception("An error occurred during user verification")

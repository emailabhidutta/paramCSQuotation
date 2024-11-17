from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password, make_password

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
            
            # Check password using Django's check_password function
            if check_password(password, user.password):
                self.stdout.write(self.style.SUCCESS('Password is correct (using Django\'s check_password)'))
            else:
                self.stdout.write(self.style.ERROR('Password is incorrect (using Django\'s check_password)'))
            
            # Check password using user's check_password method
            if user.check_password(password):
                self.stdout.write(self.style.SUCCESS('Password is correct (using user.check_password)'))
            else:
                self.stdout.write(self.style.ERROR('Password is incorrect (using user.check_password)'))
            
            # Generate a new hash and compare
            new_hash = make_password(password)
            self.stdout.write(f"Newly generated hash: {new_hash}")
            
        except UserModel.DoesNotExist:
            self.stdout.write(self.style.ERROR('User does not exist'))

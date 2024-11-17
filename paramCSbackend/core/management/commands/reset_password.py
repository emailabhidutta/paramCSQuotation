from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Reset user password'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)
        parser.add_argument('new_password', type=str)

    def handle(self, *args, **options):
        UserModel = get_user_model()
        username = options['username']
        new_password = options['new_password']

        try:
            user = UserModel.objects.get(Name=username)
            user.password = make_password(new_password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully reset password for user: {username}'))
        except UserModel.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User with username {username} does not exist'))

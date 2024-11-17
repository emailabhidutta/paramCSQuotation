from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
import logging

logger = logging.getLogger(__name__)

class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(Name=username)
            logger.debug(f"Attempting to authenticate user: {username}")
            logger.debug(f"User found: {user}")
            logger.debug(f"Is user active: {user.is_active}")
            if user.check_password(password):
                logger.debug(f"Password check successful for user: {username}")
                return user
            else:
                logger.debug(f"Password check failed for user: {username}")
        except UserModel.DoesNotExist:
            logger.debug(f"User does not exist: {username}")
        except Exception as e:
            logger.error(f"Error during authentication: {str(e)}")
        return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            logger.debug(f"User with id {user_id} does not exist")
            return None
        except Exception as e:
            logger.error(f"Error getting user: {str(e)}")
            return None

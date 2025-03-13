from django.apps import AppConfig
from django.db.utils import OperationalError

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        # Try to create a default superuser if none exists.
        # This code runs when the app is loaded.
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            if not User.objects.filter(is_superuser=True).exists():
                User.objects.create_superuser(
                    username='shahul',
                    email='shahulsauri@gmail.com',
                    password='Shahul@786'
                )
                print("Default superuser 'shahul' created.")
        except OperationalError:
            # The auth_user table doesn't exist yet (migrations haven't run), so skip.
            pass

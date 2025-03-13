from django.apps import AppConfig
from django.db.utils import OperationalError, ProgrammingError
import os

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        # Only create a default superuser if an environment variable is set.
        create_default_superuser = os.getenv("CREATE_DEFAULT_SUPERUSER", "False").lower() in ["true", "1", "yes"]
        if create_default_superuser:
            try:
                from django.contrib.auth import get_user_model
                User = get_user_model()
                if not User.objects.filter(is_superuser=True).exists():
                    User.objects.create_superuser(
                        username=os.getenv("DEFAULT_SUPERUSER_USERNAME", "shahul"),
                        email=os.getenv("DEFAULT_SUPERUSER_EMAIL", "shahulsauri@gmail.com"),
                        password=os.getenv("DEFAULT_SUPERUSER_PASSWORD", "Shahul@786")
                    )
                    print("Default superuser 'shahul' created.")
            except (OperationalError, ProgrammingError) as e:
                # The auth_user table doesn't exist yet (migrations haven't run), so skip.
                print("Skipping default superuser creation:", e)

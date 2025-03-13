from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        # Avoid creating a superuser multiple times; only create one if none exists.
        from django.contrib.auth import get_user_model
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username='shahul',
                email='shahulsauri@gmail.com',
                password='Shahul@786'
            )
            print("Default superuser 'shahul' created.")

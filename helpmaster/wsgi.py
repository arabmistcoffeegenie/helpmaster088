import os
import django
from django.core.wsgi import get_wsgi_application
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'helpmaster.settings')
django.setup()

# Automatically run migrations on startup (temporary workaround)
try:
    call_command('migrate', interactive=False)
    print("Migrations applied successfully.")
except Exception as e:
    print("Error running migrations:", e)

application = get_wsgi_application()

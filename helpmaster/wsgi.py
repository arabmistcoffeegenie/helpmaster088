import os
import django
from django.core.wsgi import get_wsgi_application
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'helpmaster.settings')
django.setup()

# Run migrations automatically on startup
try:
    call_command('migrate', interactive=False)
except Exception as e:
    # Log or handle the exception as needed.
    print("Error running migrations:", e)

application = get_wsgi_application()

"""
WSGI config for nasihat project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# settings_module = 'nasihat.deployment' if 'WEBSITE_HOSTNAME' in os.environ else 'nasihat.settings'

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'nasihat.settings')

application = get_wsgi_application()

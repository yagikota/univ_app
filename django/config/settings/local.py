from .base import *

DEBUG = True

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

SECRET_KEY = env("SECRET_KEY")
# これだと Invalid HTTP_HOST header: 'localhost:8000'. You may need to add 'localhost' to ALLOWED_HOSTS.
ALLOWED_HOSTS = ['*', 'localhost', 'example.com']

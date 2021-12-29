from .base import *

SECRET_KEY = env("SECRET_KEY")
DEBUG = True

# これだと Invalid HTTP_HOST header: 'localhost:8000'. You may need to add 'localhost' to ALLOWED_HOSTS.
# ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
ALLOWED_HOSTS = ['*', 'localhost']

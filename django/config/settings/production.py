from .base import *

DEBUG = env('DEBUG')

STATIC_ROOT = "/var/www/{}/static".format(PROJECT_NAME)

#↓ は一般的なLinuxサーバーにデプロイする場合のパス。クラウドにデプロイする場合、下記は要修正。
MEDIA_ROOT = "/var/www/{}/media".format(PROJECT_NAME)

SECRET_KEY = env('SECRET_KEY')
ALLOWED_HOSTS = env('ALLOWED_HOSTS')

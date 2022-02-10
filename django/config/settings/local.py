from .base import *

DEBUG = True

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = "/var/www/{}/static".format(PROJECT_NAME)


MEDIA_ROOT = os.path.join(BASE_DIR, "media")

SECRET_KEY = env("SECRET_KEY")

# これだと Invalid HTTP_HOST header: 'localhost:8000'. You may need to add 'localhost' to ALLOWED_HOSTS.
ALLOWED_HOSTS = ['*', 'localhost', 'example.com']

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    # ログに出力されるときのフォーマットを設定
    'formatters': {
        'develop': {
            'format': '%(asctime)s [%(levelname)s] %(pathname)s:%(lineno)d %(message)s'
        },
    },
    # 「ログをファイル出力する」、「コンソールに表示する」などのロガーが実行された時の動作を設定
    # level: ハンドラが実行されるログレベル.定義されているレベル以上で実行される
    # logging.StreamHandler	ログを標準出力に出力させる。
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'develop',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        # 内部処理全般のアクセスログ
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}

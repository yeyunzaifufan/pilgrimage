from .base import *


DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pilgrimage',
        'USER': 'root',
        'PASSWORD': 'ly123456',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'CONN_MAX_AGE': 3600,
        'OPTIONS': {
            "charset": 'utf8mb4',
            "connect_timeout": 6,
        },
    },
}

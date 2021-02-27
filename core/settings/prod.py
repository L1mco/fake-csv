import os


SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = os.environ['DEBUG']

ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['USER_PASSWORD'],
        'HOST': os.environ['DB_HOST'],
        'PORT': 5432,
    }
}

BROKER_URL = os.environ['BROKER_URL']
CELERY_RESULT_BACKEND = os.environ['CELERY_RESULT_BACKEND']
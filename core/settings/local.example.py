SECRET_KEY = 'not a secret :('

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '<DB_NAME>',
        'USER': '<USER>',
        'PASSWORD': '<PASSWORD>',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}

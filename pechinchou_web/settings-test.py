from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_ROOT = '/home/aluisio/static'
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_URL = 'http://pechinchou.nadic.ifrn.edu.br/media/'
MEDIA_ROOT = "{}/media".format(BASE_DIR)



CORS_ORIGIN_ALLOW_ALL = False # If this is used then `CORS_ORIGIN_WHITELIST` will not have any effect
#CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000',
    'https://pechinchou-next.vercel.app'
] # If this is used, then not need to use `CORS_ORIGIN_ALLOW_ALL = True`
CORS_ORIGIN_REGEX_WHITELIST = [
    'http://localhost:3000',
    'https://pechinchou-next.vercel.app'
]
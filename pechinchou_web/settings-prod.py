from .settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['.pechinchou.com.br','127.0.0.1']



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pechinchou_20211020',
        # 'NAME': os.path.join(BASE_DIR, 'mydb'),
        'USER': 'pechinchoubd',
        'PASSWORD': 'ifrnpechinchoubd2021',
        'HOST': '127.0.0.1',
        'PORT': '5432', 
    }
}



STATIC_ROOT = '/home/ubuntu/pechinchou/static'
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_URL = 'http://admin.pechinchou.com.br/media/'
MEDIA_ROOT = "/home/ubuntu/pechinchou/media"

#user mailtrap https://mailtrap.io/
EMAIL_USE_TLS=True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'pechinchouemail@gmail.com'
EMAIL_HOST_PASSWORD = 'qtmonvpqxviddksy'
EMAIL_PORT = '587'


DOMAIN_URL = "https://pechinchou.com.br"
ADMIN_URL = "https://admin.pechinchou.com.br"   


CORS_ORIGIN_ALLOW_ALL = True # If this is used then `CORS_ORIGIN_WHITELIST` will not have any effect
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = [
   'http://localhost:3000',
   'https://pechinchou-next.vercel.app',
   'https://old.pechinchou.com.br'
] # If this is used, then not need to use `CORS_ORIGIN_ALLOW_ALL = True`
CORS_ORIGIN_REGEX_WHITELIST = [
    'http://localhost:3000',
    'https://pechinchou-next.vercel.app',
    'https://old.pechinchou.com.br'
]
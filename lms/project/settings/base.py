import os

from django.urls import reverse_lazy

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/


SECRET_KEY = NotImplemented
DEBUG = False


ALLOWED_HOSTS = ["lmsbeta.pythonanywhere.com","127.0.0.1","mysite.com"]


# Application definition

INSTALLED_APPS = [

    "admin_interface",
    "colorfield",

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
  

    #thrid party packages
    'compressor',
    'crispy_forms',
    'crispy_bootstrap5',
    'embed_video',
    'ckeditor',
    'ckeditor_uploader',
    # 'rest_framework',
    'channels',
    # 'debug_toolbar',
    # 'social_django',
    'django_extensions',
     'widget_tweaks',
      'tempus_dominus',

   

    

    #custom apps
    'chat.apps.ChatConfig',
    # 'accounts.apps.AccountsConfig',
    'courses.apps.CoursesConfig',
    'students.apps.StudentsConfig',
    'crendential',

    #exam related
    'exam.essay',
    'exam.multichoice',
    'exam.quiz',
    'exam.true_false'
]

MIDDLEWARE = [
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'lms.project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR /'templates'],# type: ignore
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'courses.context_processors.my_context_processor',
                 # `allauth` needs this from django
                
            ],
        },
    },
]

WSGI_APPLICATION = 'lms.project.wsgi.application'
ASGI_APPLICATION = 'lms.project.asgi.application'
# ASGI_APPLICATION = 'lms.project.asgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR /'db.sqlite3',# type:ignore
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR,'static')# type:ignore

# MEDIA_URL = 'media/'
# MEDIA_ROOT = os.path.join(BASE_DIR,'media')# type:ignore

STATICFILES_DIRS = [
  BASE_DIR / 'static' / 'css' / 'landing',
  BASE_DIR /'static' / 'css' / 'courses',
  BASE_DIR /'static' / 'css' /'students',
  BASE_DIR /'static' / 'css' / 'exam',
  BASE_DIR /'static' / 'css' / 'chat',
  BASE_DIR /'static'  / 'css' / 'allauth',

  BASE_DIR / 'static' / 'assets' ,
  BASE_DIR / 'static' / 'assets' / 'allauth',
  BASE_DIR / 'static' / 'js' ,
  BASE_DIR / 'static' / 'js' 
]




DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_REDIRECT_URL = reverse_lazy('student_course_list')





INTERNAL_IPS = [
'127.0.0.1',
]


CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 60 * 15
# 15 minutes
CACHE_MIDDLEWARE_KEY_PREFIX = 'lms'

# AUTH_USER = "accounts.CustomUser"


# Email server configuration
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'tinsingjobs2k@gmail.com'
EMAIL_HOST_PASSWORD = 'vavkndyvafegycua'
EMAIL_PORT = 587
EMAIL_USE_TLS = True


PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.ScryptPasswordHasher',
]




AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',#username authentication
    # 'accounts.authentication.EmailAuthBackend',#email authentication
    'allauth.account.auth_backends.AuthenticationBackend',
   
    ]



# Django Allauth settings
ACCOUNT_AUTHENTICATION_METHOD = 'username'
ACCOUNT_EMAIL_REQUIRED= True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS=10 
ACCOUNT_LOGIN_ATTEMPTS_LIMIT=5
ACCOUNT_EMAIL_VERIFICATION="optional"
ACCOUNT_REDIRECT_URL='/course/course_list/'
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT=86400
ACCOUNT_UNIQUE_EMAIL=False
ACCOUNT_EMAIL_CONFORMATION=180
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True




# This setting will redirect users to the homepage after a successful login.

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

REDIRECT_UNAUTHENTICATED_USER = '/signup/success/'



SITE_ID = 1

# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    "github": {
        # For each provider, you can choose whether or not the
        # email address(es) retrieved from the provider are to be
        # interpreted as verified.
        "VERIFIED_EMAIL": True
    },
    "google": {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        "APPS": [
            {
                "client_id": "123",
                "secret": "456",
                "key": ""
            },
        ],
        # These are provider-specific settings that can only be
        # listed here:
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
    }
}

LOGIN_URL = '/'


#admin custimization
X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]

CRISPY_TEMPLATE_PACK = 'bootstrap5' 


TEMPUS_DOMINUS_LOCALIZE = True
TEMPUS_DOMINUS_INCLUDE_ASSETS = False
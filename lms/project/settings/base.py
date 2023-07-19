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
    
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
  

    #thrid party packages
    'compressor',
    "crispy_forms",
    "crispy_tailwind",
    'embed_video',
    'ckeditor',
    'ckeditor_uploader',
    'rest_framework',
    'channels',
    'debug_toolbar',
    # 'social_django',
    'django_extensions',

   

    

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
    'debug_toolbar.middleware.DebugToolbarMiddleware',
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
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'courses.context_processors.my_context_processor',
                 # `allauth` needs this from django
                'django.template.context_processors.request',
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

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR,'static')# type:ignore




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

ACCOUNT_EMAIL_REQUIRED= True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS=10 
ACCOUNT_LOGIN_ATTEMPTS_LIMIT=5
ACCOUNT_EMAIL_VERIFICATION="mandatory"
ACCOUNT_REDIRECT_URL='/course/course_list/'
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT=86400
ACCOUNT_UNIQUE_EMAIL=True
ACCOUNT_EMAIL_CONFORMATION=180
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True


ACCOUNT_FORMS = {
    'signup': 'lms.forms.LmsSignupForm',
  
    }


# This setting will redirect users to the homepage after a successful login.

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

REDIRECT_UNAUTHENTICATED_USER = '/signup/success/'




SITE_ID = 1

# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'APP': {
            'client_id': '123',
            'secret': '456',
            'key': ''
        }
    }
}


LOGIN_URL = '/'


#admin custimization
X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]

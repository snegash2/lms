import os

from django.urls import reverse_lazy

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

ROLEPERMISSIONS_MODULE = 'courses.roles'
SECRET_KEY = NotImplemented
DEBUG = False


ALLOWED_HOSTS = ["lmsbeta.pythonanywhere.com","127.0.0.1","mysite.com"]

CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8083/course/delete_doc/',
]
# Application definition

INSTALLED_APPS = [
 
    'rolepermissions',
    'django_roles_access',
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
     'django.contrib.humanize',
  

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
    # 'tempus_dominus',
    "bootstrap_datepicker_plus",
    'django_tables2',
    'crudbuilder',
     'newsfeed',

    

    #custom apps
    'chat.apps.ChatConfig',
    'landing.apps.LandingConfig',
    'courses.apps.CoursesConfig',
    'students.apps.StudentsConfig',
    'crendential',
    # 'avatars',

    #exam related
    'exam.essay',
    'exam.multichoice',
    'exam.quiz',
    'exam.true_false',
    
    
    
    # 'spirit.core',
    # 'spirit.admin',
    # 'spirit.search',

    # 'spirit.user',
    # 'spirit.user.admin',
    # 'spirit.user.auth',

    # 'spirit.category',
    # 'spirit.category.admin',

    # 'spirit.topic',
    # 'spirit.topic.admin',
    # 'spirit.topic.favorite',
    # 'spirit.topic.moderate',
    # 'spirit.topic.notification',
    # 'spirit.topic.private',
    # 'spirit.topic.unread',

    # 'spirit.comment',
    # 'spirit.comment.bookmark',
    # 'spirit.comment.flag',
    # 'spirit.comment.flag.admin',
    # 'spirit.comment.history',
    # 'spirit.comment.like',
    # 'spirit.comment.poll',

    # 'djconfig',
    # 'haystack',
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
    
    
       # 'spirit.core.middleware.XForwardedForMiddleware',
    # 'spirit.user.middleware.TimezoneMiddleware',
    # 'spirit.user.middleware.LastIPMiddleware',
    # 'spirit.user.middleware.LastSeenMiddleware',
    # 'spirit.user.middleware.ActiveUserMiddleware',
    # 'spirit.core.middleware.PrivateForumMiddleware',
    # 'djconfig.middleware.DjConfigMiddleware',
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
                'django.template.context_processors.request',
                'landing.utils.global_forms'

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
  BASE_DIR /'static' / 'css' / 'courses' / 'manage',
  BASE_DIR /'static' / 'css' /'students',
  BASE_DIR /'static' / 'css' / 'exam',
  BASE_DIR /'static' / 'css' / 'chat',
  BASE_DIR /'static'  / 'css' / 'allauth',
  BASE_DIR /'static'  / 'css' / 'quiz',
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
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED= True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS=10 
ACCOUNT_LOGIN_ATTEMPTS_LIMIT=5
ACCOUNT_EMAIL_VERIFICATION="optional"
ACCOUNT_REDIRECT_URL='/course/course_list/'
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT=86400
ACCOUNT_UNIQUE_EMAIL=True
ACCOUNT_EMAIL_CONFORMATION=180
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True

ACCOUNT_FORMS = {
    'signup': 'landing.utils.MyCustomSignupForm'
   # 'login': 'landing.utils.MyCustomSignupForm',
  
}

AUTH_USER_MODEL = 'landing.LmsUser'


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



#admin custimization
X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]

CRISPY_TEMPLATE_PACK = 'bootstrap5' 


TEMPUS_DOMINUS_LOCALIZE = True
TEMPUS_DOMINUS_INCLUDE_ASSETS = False



HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(BASE_DIR, 'st_search'),
    },
}
HAYSTACK_SIGNAL_PROCESSOR = 'spirit.search.signals.RealtimeSignalProcessor'
ST_SITE_URL = 'http://example.com'


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'spirit_cache',
    },
    # 'st_rate_limit': {
    #     'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
    #     'LOCATION': 'spirit_rl_cache',
    #     'TIMEOUT': None
    # }
}


CACHES.update({
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
    # 'st_rate_limit': {
    #     'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    #     'LOCATION': 'spirit_rl_cache',
    #     'TIMEOUT': None
    # }
})




DJANGO_TABLES2_TABLE_ATTRS = {
    'class': 'table  table-hover table-centered',
    'thead': {
        'class': 'table-light',
    },
   
    'td': {
        'class':'table-active'
    }
}
from pathlib import Path
import os.path

from split_settings.tools import include,optional
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


# Namespacing our own custom enviroment variable

ENVVAR_SETTINGS_PREFIX = 'CORESETTINGS_'
LOCAL_SETTINGS_PATH = os.getenv(f'{ENVVAR_SETTINGS_PREFIX}LOCAL_SETTINGS_PATH')

if not LOCAL_SETTINGS_PATH:
    LOCAL_SETTINGS_PATH = 'local/settings.dev.py'

if not os.path.isabs(LOCAL_SETTINGS_PATH):
    LOCAL_SETTINGS_PATH = str(BASE_DIR / LOCAL_SETTINGS_PATH)

include(
    'base.py',
    'rest_api.py',
    'ckeditor.py',
    'custom.py',
    # 'cache.py',
    optional(LOCAL_SETTINGS_PATH),
    'envvars.py',
    'docker.py',
    # 'flowbite.py'

)
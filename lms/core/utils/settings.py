import  os
from .misc import yaml_coerce


def get_settings_from_enviroment(prefix):
    prefix_len = len(prefix)
    return {key[prefix_len:]:yaml_coerce(value) for key,value in os.environ.items() if key.startswith(prefix)}


def get_filename(filename, request):
    return filename.upper()
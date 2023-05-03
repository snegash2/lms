from lms.core.utils.settings import get_settings_from_enviroment
from lms.core.utils.collections import deep_update


deep_update(globals(),get_settings_from_enviroment(ENVVAR_SETTINGS_PREFIX)) # type: ignore
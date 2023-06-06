CACHES = {
'default': {
'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
'LOCATION': '127.0.0.1:11211',
}
}


# CACHES = {
#     'default': {
#     'BACKEND': 'django.core.cache.backends.redis.RedisCache',
#     'LOCATION': 'redis://127.0.0.1:6379',
#     }
# }
# settings specic to this application only  (no django or thrid pary)

IN_DOCKER = False


CHANNEL_LAYERS = {
'default': {
'BACKEND': 'channels_redis.core.RedisChannelLayer',
'CONFIG': {
'hosts': [('127.0.0.1', 6379)],
},
},
}

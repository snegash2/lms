


from django.urls import re_path
from . import consumers
websocket_urlpatterns = [
    re_path(r'egiliablityy/(?P<course_id>\d+)/$',consumers.CourseConsumer.as_asgi()),
]
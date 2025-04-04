from django.urls import re_path
from apps.groups.consumers import GroupConsumer

websocket_urlpatterns = [
    re_path(r'ws/group/(?P<invite_code>\w+)/$', GroupConsumer.as_asgi()),
]
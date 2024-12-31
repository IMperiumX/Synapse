from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/page/(?P<page_id>\d+)/edit/$", consumers.PageEditConsumer.as_asgi()),
]

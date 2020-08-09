from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path('IDE/output/', consumers.OutputConsumer),
]
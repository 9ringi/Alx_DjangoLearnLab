# notifications/urls.py
from django.urls import path
from .views import get_notifications, mark_notifications_as_read

urlpatterns = [
    path('', get_notifications, name='get_notifications'),  # To view notifications
    path('mark-as-read/', mark_notifications_as_read, name='mark_notifications_as_read'),  # To mark notifications as read
]

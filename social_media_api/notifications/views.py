from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from .models import Notification

def get_notifications(request):
    if request.user.is_authenticated:
        notifications = request.user.notifications.filter(read=False)
        data = [
            {
                "actor": n.actor.username,
                "verb": n.verb,
                "target": str(n.target),
                "timestamp": n.timestamp,
            }
            for n in notifications
        ]
        return JsonResponse({"notifications": data}, status=200)
    return JsonResponse({"message": "Unauthorized"}, status=403)

def mark_notifications_as_read(request):
    if request.user.is_authenticated:
        notifications = request.user.notifications.filter(read=False)
        notifications.update(read=True)
        return JsonResponse({"message": "Notifications marked as read"}, status=200)
    return JsonResponse({"message": "Unauthorized"}, status=403)

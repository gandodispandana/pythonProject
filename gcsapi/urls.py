from django.contrib import admin
from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('notification/', NotificationAPIView.as_view()),
    path('notificationtemp/', NotificationTemplateAPIView.as_view()),
    path('reroute/', ReRoute.as_view())
]

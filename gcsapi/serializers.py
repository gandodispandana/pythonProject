from django.contrib.auth import authenticate
from rest_framework import serializers, exceptions
from .models import *
from zoneinfo import available_timezones

class PhoneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneType
        fields = '__all__'


class ScheduledNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledNotification
        fields = '__all__'


class NotificationTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationTemplate
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    tzone = serializers.ChoiceField(choices=available_timezones())

    class Meta:
        model = Notification
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username", "")
        password = data.get("password", "")

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data["user"] = user
                else:
                    msg = "User is deactivated."
                    raise exceptions.ValidationError(msg)
            else:
                msg = "Unable to login with given credentials."
                raise exceptions.ValidationError(msg)
        else:
            msg = "Must provide username and password both."
            raise exceptions.ValidationError(msg)
        return data

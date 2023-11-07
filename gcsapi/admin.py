from django.contrib import admin
from .models import *

admin.site.register(PhoneType)
admin.site.register(Member)
admin.site.register(MemberSourceIdentifier)
admin.site.register(NotificationTemplate)
admin.site.register(Notification)
admin.site.register(NotificationCallback)
admin.site.register(ScheduledNotification)
admin.site.register(BrokerClient)
admin.site.register(BrokerClientTemplate)
admin.site.register(Role)

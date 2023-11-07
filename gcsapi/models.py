from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from timezone_field import TimeZoneField


class Role(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, null=False, blank=False)


class PhoneType(models.Model):
    number = models.CharField(max_length=20, null=False, blank=False)
    phone_type = models.CharField(max_length=20, null=False, blank=False)
    opt_out = models.BooleanField(default=False)
    last_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)


class Member(models.Model):
    first_name = models.CharField(max_length=20, null=False, blank=False)
    last_name = models.CharField(max_length=20, null=False, blank=False)
    phone = models.ForeignKey(PhoneType, on_delete=models.CASCADE)


class MemberSourceIdentifier(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    source_name = models.CharField(max_length=20, null=False, blank=False)
    source_id = models.CharField(max_length=20, null=False, blank=False)
    last_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)


class NotificationTemplate(models.Model):
    notification_body = models.TextField()
    template_type = models.CharField(max_length=20, null=False, blank=False)
    name = models.CharField(max_length=50, null=False, blank=False)
    language = models.CharField(max_length=20, null=False, blank=False)
    last_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)


class BrokerClient(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    notification_template = models.ManyToManyField("NotificationTemplate",
                                                   through="BrokerClientTemplate", related_name="broker_client",
                                                   related_query_name="broker_clients")

    def __str__(self) -> str:
        return self.code


class Notification(models.Model):
    id = models.CharField(max_length=50, null=False, blank=False, primary_key=True)
    sid = models.CharField(max_length=25, null=False, blank=False)
    source_app = models.CharField(max_length=50, null=False, blank=False)
    status = models.CharField(max_length=50, default="created")
    notification_type = models.CharField(max_length=50)
    phone_number = models.ForeignKey(PhoneType, on_delete=models.CASCADE)
    trip_date = models.DateField(max_length=20)
    trip_id = models.CharField(max_length=25)
    tp_type = models.CharField(max_length=50)
    trip_pu_time = models.DateTimeField(default=timezone.now)
    pu_address = models.CharField(max_length=250, null=False, blank=False)
    do_address = models.CharField(max_length=250, null=False, blank=False)
    tp_name = models.CharField(max_length=50, null=False, blank=False)
    tp_phone_number = models.CharField(max_length=50, null=False, blank=False)
    tzone = TimeZoneField(default='US/Central')
    member_source_identifier = models.ForeignKey(MemberSourceIdentifier, on_delete=models.CASCADE)
    broker_client = models.ForeignKey(BrokerClient, on_delete=models.CASCADE)
    account_id = models.CharField(max_length=50)
    payload_body = models.JSONField()
    message_body = models.JSONField()
    force_communication = models.CharField(max_length=25, null=False, blank=False)
    date_created = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(default=timezone.now)


class BrokerClientTemplate(models.Model):
    broker_client = models.ForeignKey(BrokerClient, on_delete=models.CASCADE)
    notification_template = models.ForeignKey(NotificationTemplate, on_delete=models.CASCADE)
    activation_date = models.DateTimeField(default=timezone.now)
    deactivation_date = models.DateTimeField(default=None, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.broker_client} | {self.notification_template}"


class NotificationCallback(models.Model):
    sid = models.CharField(max_length=50, null=False, blank=False)
    status = models.CharField(max_length=25, null=False, blank=False)
    sent = models.BooleanField(default=False)
    sent_time = models.DateTimeField(null=True, auto_now=True)
    queued = models.BooleanField(default=False)
    queued_time = models.DateTimeField(null=True, auto_now=True)
    delivered = models.BooleanField(default=False)
    delivered_time = models.DateTimeField(null=True, auto_now=True)
    undelivered = models.BooleanField(default=False)
    undelivered_time = models.DateTimeField(null=True, auto_now=True)
    failed = models.BooleanField(default=False)
    failed_time = models.DateTimeField(null=True, auto_now=True)


class ScheduledNotification(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    scheduled_time = models.DateTimeField()
    status = models.CharField(max_length=20, default="scheduled")
    date_created = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.notification.id

    def save(self, *args, **kwargs):
        self.last_modified = timezone.now()

        super().save(*args, **kwargs)

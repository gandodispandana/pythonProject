# Generated by Django 4.2.5 on 2023-09-22 05:46

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import timezone_field.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('sid', models.CharField(max_length=25)),
                ('source_app', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=25)),
                ('notification_type', models.CharField(max_length=50)),
                ('trip_date', models.DateField()),
                ('trip_id', models.CharField(max_length=50)),
                ('tp_type', models.CharField(max_length=50)),
                ('trip_pu_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('pu_address', models.CharField(max_length=50)),
                ('do_address', models.CharField(max_length=50)),
                ('tp_name', models.CharField(max_length=50)),
                ('tp_phone_number', models.CharField(max_length=50)),
                ('tzone', timezone_field.fields.TimeZoneField(default='US/Central')),
                ('payload_body', models.JSONField()),
                ('message_body', models.JSONField()),
                ('force_communication', models.CharField(max_length=25)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='NotificationCallback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sid', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=25)),
                ('sent', models.BooleanField(default=False)),
                ('sent_time', models.DateTimeField(auto_now=True, null=True)),
                ('queued', models.BooleanField(default=False)),
                ('queued_time', models.DateTimeField(auto_now=True, null=True)),
                ('delivered', models.BooleanField(default=False)),
                ('delivered_time', models.DateTimeField(auto_now=True, null=True)),
                ('undelivered', models.BooleanField(default=False)),
                ('undelivered_time', models.DateTimeField(auto_now=True, null=True)),
                ('failed', models.BooleanField(default=False)),
                ('failed_time', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='NotificationTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_body', models.CharField(max_length=50)),
                ('template_type', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=20)),
                ('language', models.CharField(max_length=20)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PhoneType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=20)),
                ('phone_type', models.CharField(max_length=20)),
                ('opt_out', models.BooleanField(default=False)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ScheduledNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scheduled_time', models.DateTimeField()),
                ('status', models.CharField(default='scheduled', max_length=20)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_modified', models.DateTimeField(default=django.utils.timezone.now)),
                ('notification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gcsapi.notification')),
            ],
        ),
        migrations.AddField(
            model_name='notification',
            name='phone_number',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gcsapi.phonetype'),
        ),
        migrations.CreateModel(
            name='MemberSourceIdentifier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_name', models.CharField(max_length=20)),
                ('source_id', models.CharField(max_length=20)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gcsapi.member')),
            ],
        ),
        migrations.AddField(
            model_name='member',
            name='phone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gcsapi.phonetype'),
        ),
    ]

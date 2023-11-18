# Generated by Django 4.2.7 on 2023-11-14 17:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('doctors_and_labs', '0003_delete_labtestsavailable_labtests_lab'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='labavailability',
            name='slots_status',
        ),
        migrations.AddField(
            model_name='labavailability',
            name='slots_details_offline',
            field=models.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name='labavailability',
            name='slots_details_online',
            field=models.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name='labavailability',
            name='slots_status_offline',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='labavailability',
            name='slots_status_online',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='labavailability',
            name='lab',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lab_availabilities', to=settings.AUTH_USER_MODEL),
        ),
    ]

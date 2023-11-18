# Generated by Django 4.2.7 on 2023-11-14 17:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0002_alter_appointments_lab_test'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('doctors_and_labs', '0002_labtests_remove_labtestsavailable_lab'),
    ]

    operations = [
        migrations.DeleteModel(
            name='LabTestsAvailable',
        ),
        migrations.AddField(
            model_name='labtests',
            name='lab',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

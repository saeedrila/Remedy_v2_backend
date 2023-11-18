# Generated by Django 4.2.7 on 2023-11-13 18:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('doctors_and_labs', '0001_initial'),
        ('payments', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointments',
            fields=[
                ('appointment_id', models.CharField(max_length=12, primary_key=True, serialize=False, unique=True)),
                ('specialization_title', models.CharField(max_length=40, null=True)),
                ('date', models.DateField()),
                ('time', models.CharField(max_length=20)),
                ('status', models.CharField(max_length=20)),
                ('slot_type', models.CharField(max_length=10)),
                ('order_created', models.DateTimeField(auto_now_add=True)),
                ('document', models.FileField(null=True, upload_to='appointment_documents/')),
                ('prescription', models.TextField(blank=True, max_length=500, null=True)),
                ('doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='doctor_appointments', to=settings.AUTH_USER_MODEL)),
                ('lab', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lab_appointments', to=settings.AUTH_USER_MODEL)),
                ('lab_test', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='doctors_and_labs.labtestsavailable')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patient_appointments', to=settings.AUTH_USER_MODEL)),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payments.payments')),
            ],
        ),
    ]

# Generated by Django 4.2.7 on 2023-11-14 17:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doctors_and_labs', '0002_labtests_remove_labtestsavailable_lab'),
        ('appointments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointments',
            name='lab_test',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='doctors_and_labs.labtests'),
        ),
    ]

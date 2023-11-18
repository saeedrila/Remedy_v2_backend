# Generated by Django 4.2.7 on 2023-11-14 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors_and_labs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LabTests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_title', models.CharField(db_index=True, max_length=50)),
                ('fee_per_session', models.PositiveIntegerField(db_index=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='labtestsavailable',
            name='lab',
        ),
    ]

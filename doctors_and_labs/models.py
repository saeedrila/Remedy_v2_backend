from django.db import models
from authentication.models import Account



#Doctor related Models
class DoctorProfile(models.Model):
    doctor = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='doctor_profiles') #Related name
    fee_per_session = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    experience = models.PositiveIntegerField(default=0, null=True)
    description = models.TextField(null=True)
    document_url = models.CharField(max_length=100, null=True, blank=True)

class DoctorAvailability(models.Model):
    date = models.DateField(db_index=True)
    doctor = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='doctor_availabilities', db_index=True)
    slots_status_online = models.BooleanField(default=False)
    slots_status_offline = models.BooleanField(default=False)
    slots_details_online = models.JSONField(default=dict)
    slots_details_offline = models.JSONField(default=dict)

class DoctorSpecializations(models.Model):
    doctor = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='doctor_specializations')
    specialization_title = models.CharField(max_length=40, default='')


# Lab related Models
class LabProfile(models.Model):
    lab = models.ForeignKey(Account, on_delete=models.CASCADE)
    experience = models.PositiveIntegerField(default=0)
    description = models.TextField(null=True)
    document_url = models.CharField(max_length=100, null=True, blank=True)

class LabAvailability(models.Model):
    date = models.DateField(db_index=True)
    lab = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='lab_availabilities', db_index=True)
    slots_status_online = models.BooleanField(default=False)
    slots_status_offline = models.BooleanField(default=False)
    slots_details_online = models.JSONField(default=dict)
    slots_details_offline = models.JSONField(default=dict)

class LabTests(models.Model):
    lab = models.ForeignKey(Account, on_delete=models.CASCADE, db_index=True)
    test_title = models.CharField(max_length=50, db_index=True)
    fee_per_session = models.PositiveIntegerField(db_index=True)
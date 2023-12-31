from rest_framework import serializers
from .models import Appointments



class PatientAppointmentsSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    class Meta:
        model = Appointments
        fields = [
            'appointment_id',
            'email',
            'time',
            'status',
            'slot_type',
            'date'
        ]
    def get_email(self, obj):
        if hasattr(obj, 'doctor') and obj.doctor:
            return obj.doctor.email
        elif hasattr(obj, 'lab') and obj.lab:
            return obj.lab.email
        else:
            return None

class DoctorAppointmentsSerializer(serializers.ModelSerializer):
    patient_email = serializers.SerializerMethodField()
    class Meta:
        model = Appointments
        fields = [
            'appointment_id',
            'patient_email',
            'time',
            'status',
            'slot_type',
            'date'
        ]
    def get_patient_email(self, obj):
        return obj.patient.email if obj.patient else None
    
class AllAppointmentsSerializer(serializers.ModelSerializer):
    patient_email = serializers.SerializerMethodField()
    doctor_email = serializers.SerializerMethodField()
    lab_email = serializers.SerializerMethodField()
    class Meta:
        model = Appointments
        fields = [
            'appointment_id',
            'patient_email',
            'doctor_email',
            'lab_email',
            'time',
            'status',
            'slot_type',
            'date',
            'order_created',
        ]
    def get_patient_email(self, obj):
        return obj.patient.email if obj.patient else None

    def get_doctor_email(self, obj):
        return obj.doctor.email if obj.doctor else None

    def get_lab_email(self, obj):
        return obj.lab.email if obj.lab else None

class PrescriptionSerializer(serializers.Serializer):
    appointment_id = serializers.CharField()
    prescription = serializers.CharField(max_length=500)

class ReportSerializer(serializers.Serializer):
    appointment_id = serializers.CharField()
    report = serializers.CharField(max_length=500)

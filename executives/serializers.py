from rest_framework import serializers
from authentication.models import Account
from doctors_and_labs.models import DoctorProfile, LabProfile
from executives.models import ExecutiveProfile



class AccountApprovalSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    email = serializers.EmailField()
    mobile = serializers.CharField()
    is_doctor = serializers.BooleanField()
    is_lab = serializers.BooleanField()
    is_executive = serializers.BooleanField()
    is_verified = serializers.BooleanField()
    is_active = serializers.BooleanField()

class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = ['document_url']

class LabProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabProfile
        fields = ['document_url']

class ExecutiveProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExecutiveProfile
        fields = ['document_url']

class AccountApprovalPatchSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    status = serializers.BooleanField()


from rest_framework import serializers
from authentication.models import Account
from doctors_and_labs.models import (
    DoctorAvailability, 
    DoctorProfile, 
    LabProfile,
    DoctorSpecializations,
    LabTests,
)


# Doctor specialization registration
class RegisterSpecialization(serializers.Serializer):
    specialization = serializers.CharField(max_length=40)


# Doctor specialization data for the frontend
class DoctorSpecializationData(serializers.Serializer):
    id = serializers.CharField()
    specialization = serializers.CharField()

# Doctor availability registration
class DoctorAvailabilityRegistration(serializers.Serializer):
    date = serializers.CharField(max_length=10)

# Doctor profile get
class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = '__all__'

# Account serializer for doctor at a specific specialization
class AccountSerializerDoctorAtSpecialization(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('email')




# Specialization get universal for the home/landing page
class SpecializationSerializer(serializers.Serializer):
    specialization_title = serializers.CharField()
# Tests for home/landing page
class TestSerializer(serializers.Serializer):
    test_title = serializers.CharField()

#Used to list tests available for a particular lab
class LabSpecificTestSerializer(serializers.ModelSerializer):
    fee_per_session = serializers.IntegerField(required=False)

    class Meta:
        model = LabTests
        fields = ('test_title','fee_per_session')

class AddTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabTests
        fields = ('lab', 'test_title', 'fee_per_session')



# Need to check the following and wanted to delete classes that are not required.
# Doctor status get, following 2 classes are part of it.
# Not using anymore
class SlotSerializer(serializers.Serializer):
    time = serializers.CharField()
    status = serializers.CharField()

class DoctorAvailabilitySerializer(serializers.Serializer):
    date = serializers.CharField()
    slots_status_online = serializers.BooleanField()
    slots_status_offline = serializers.BooleanField()
    slots_details_online = SlotSerializer(many=True)
    slots_details_offline = SlotSerializer(many=True)

class DoctorAvailabilityToggleSerializer(serializers.Serializer):
    status = serializers.BooleanField()
    slot_id = serializers.CharField()
    date = serializers.CharField()
    line = serializers.CharField()
    time = serializers.CharField()

class LabAvailabilityToggleSerializer(serializers.Serializer):
    status = serializers.BooleanField()
    slot_id = serializers.CharField()
    date = serializers.CharField()
    line = serializers.CharField()
    time = serializers.CharField()


class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = ('fee_per_session', 'experience', 'description')

class LabProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabProfile
        fields = ('experience', 'description')


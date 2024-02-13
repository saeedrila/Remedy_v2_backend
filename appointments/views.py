from django.shortcuts import render
from rest_framework.views import APIView
from authentication.models import Account
from appointments.models import Appointments
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta
from django.db.models import Sum
from django.shortcuts import get_object_or_404

from .serializers import (
    PatientAppointmentsSerializer,
    DoctorAppointmentsSerializer,
    AllAppointmentsSerializer,
    PrescriptionSerializer,
    ReportSerializer,
)
from payments.models import Payments


class FetchPatientAppointData(APIView):
    def get(self, request):
        try:
            account = Account.objects.get(id = request.user.id)
            appointments_list = Appointments.objects.filter(patient_id=account).order_by('-order_created')
            serializer = PatientAppointmentsSerializer(appointments_list, many=True)
            # print('Appointment data: ', serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print('Exception: ', e)
            return Response({'error': 'Error occurred'}, status=status.HTTP_400_BAD_REQUEST)


#Fetch appointments for doctor dashboard
class FetchDoctorAppointData(APIView):
    def get(self, request):
        try:
            account = Account.objects.get(id = request.user.id)
            # print('Account: ', account)
            appointments_list = Appointments.objects.filter(doctor_id=account).order_by('-order_created')
            # print('Appointment list: ', appointments_list)
            serializer = DoctorAppointmentsSerializer(appointments_list, many=True)
            # print('Serialized data: ', serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'Error occurred'}, status=status.HTTP_400_BAD_REQUEST)
        
#Fetch appointments for doctor dashboard
class FetchLabAppointData(APIView):
    def get(self, request):
        try:
            account = Account.objects.get(id = request.user.id)
            # print('Account: ', account)
            appointments_list = Appointments.objects.filter(lab_id=account).order_by('-order_created')
            # print('Appointment list: ', appointments_list)
            serializer = DoctorAppointmentsSerializer(appointments_list, many=True)
            # print('Serialized data: ', serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'Error occurred'}, status=status.HTTP_400_BAD_REQUEST)
        
#Fetch appointment for Executive dashboard
class FetchAllAppointData(APIView):
    def get(self, request):
        try:
            appointments_list = Appointments.objects.order_by('-order_created')
            # print('Appointment list: ', appointments_list)
            serializer = AllAppointmentsSerializer(appointments_list, many=True)
            # print('Serialized data: ', serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'Error occurred'}, status=status.HTTP_400_BAD_REQUEST)


# Handles Doctor's prescription
class AppointmentPrescription(APIView):
    def get(self, request):
        appointment_id = request.query_params.get('appointment_id')
        try:
            appointment = Appointments.objects.get(appointment_id=appointment_id)
            serializer = PrescriptionSerializer({
                'appointment_id': appointment.appointment_id,
                'prescription': appointment.prescription,
            })

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Appointments.DoesNotExist:
            return Response({"error": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def patch(self, request):
        print(request.data)
        serializer = PrescriptionSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        appointment_id = serializer.validated_data.get('appointment_id')
        prescription = serializer.validated_data.get('prescription')

        try:
            appointment = Appointments.objects.get(appointment_id=appointment_id)
            appointment.prescription = prescription
            appointment.status = 'Completed'
            appointment.save()
            payment_obj = Payments.objects.get(appointment=appointment_id)
            payment_obj.staff_payment = int(payment_obj.amount * 0.9)
            payment_obj.platform_fee = int(payment_obj.amount - payment_obj.staff_payment)
            payment_obj.appointment_completion = True
            payment_obj.save()
            return Response({"message": "Prescription updated successfully"}, status=status.HTTP_200_OK)

        except Appointments.DoesNotExist:
            return Response({"error": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND)

# Handles Lab's reports
class AppointmentReport(APIView):
    def get(self, request):
        appointment_id = request.query_params.get('appointment_id')
        try:
            appointment = Appointments.objects.get(appointment_id=appointment_id)
            serializer = ReportSerializer({
                'appointment_id': appointment.appointment_id,
                'report': appointment.report,
            })

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Appointments.DoesNotExist:
            return Response({"error": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def patch(self, request):
        # print(request.data)
        serializer = ReportSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        appointment_id = serializer.validated_data.get('appointment_id')
        report = serializer.validated_data.get('report')

        try:
            appointment = Appointments.objects.get(appointment_id=appointment_id)
            appointment.report = report
            appointment.status = 'Completed'
            appointment.save()
            payment_obj = Payments.objects.get(appointment=appointment_id)
            payment_obj.staff_payment = int(payment_obj.amount * 0.9)
            payment_obj.platform_fee = int(payment_obj.amount - payment_obj.staff_payment)
            payment_obj.appointment_completion = True
            payment_obj.save()
            return Response({"message": "Report updated successfully"}, status=status.HTTP_200_OK)

        except Appointments.DoesNotExist:
            return Response({"error": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND)

# Fetch data for dashboard
class FetchExecutiveDashboardData(APIView):
    def get(self, request):
        total_appointments_catered = Appointments.objects.filter(status='Completed').count()

        seven_days_ago = datetime.now() - timedelta(days=7)
        completed_appointments_last_week = Appointments.objects.filter(
            status='Completed',
            date__gte=seven_days_ago,
        )
        total_platform_fee = completed_appointments_last_week.aggregate(Sum('payment__platform_fee'))['payment__platform_fee__sum']
        if total_platform_fee is not None:
            total_platform_fee_last_week = int(total_platform_fee//100)
        else:
            total_platform_fee_last_week = 0

        total_appointments_today = Appointments.objects.filter(date=datetime.now()).count()
        total_appointments_today_completed = Appointments.objects.filter(status='Completed', date=datetime.now()).count()
        total_appointment_today_completed_perc = 0
        if total_appointments_today != 0:
            total_appointment_today_completed_perc = int((total_appointments_today_completed / total_appointments_today) * 100)
            
        data = {
            'total_appointments_catered': total_appointments_catered,
            'total_platform_fee_last_week': total_platform_fee_last_week,
            'total_appointments_today': total_appointments_today,
            'total_appointments_today_completed': total_appointments_today_completed,
            'total_appointment_today_completed_perc': total_appointment_today_completed_perc
        }
        return Response(data, status=status.HTTP_200_OK)

# Fetch data for dashboard
class FetchDoctorDashboardData(APIView):
    def get(self, request):
        account = Account.objects.get(id=request.user.id)
        total_appointments_catered = Appointments.objects.filter(status='Completed', doctor=account).count()

        seven_days_ago = datetime.now() - timedelta(days=7)
        completed_appointments_last_week = Appointments.objects.filter(
            status='Completed',
            date__gte=seven_days_ago,
        )
        total_staff_payment = completed_appointments_last_week.aggregate(Sum('payment__staff_payment'))['payment__staff_payment__sum']
        if total_staff_payment is not None:
            total_staff_payment_last_week = int(total_staff_payment // 100)
        else:
            total_staff_payment_last_week = 0

        total_appointments_today = Appointments.objects.filter(date=datetime.now(), doctor=account).count()
        total_appointments_today_completed = Appointments.objects.filter(status='Completed', date=datetime.now(), doctor=account).count()
        total_appointment_today_completed_perc = 0
        if total_appointments_today != 0:
            total_appointment_today_completed_perc = int((total_appointments_today_completed / total_appointments_today) * 100)

        data = {
            'total_appointments_catered': total_appointments_catered,
            'total_staff_payment_last_week': total_staff_payment_last_week,
            'total_appointments_today': total_appointments_today,
            'total_appointments_today_completed': total_appointments_today_completed,
            'total_appointment_today_completed_perc': total_appointment_today_completed_perc
        }
        # print('Data: ', data)
        return Response(data, status=status.HTTP_200_OK)

# Fetch data for dashboard
class FetchLabDashboardData(APIView):
    def get(self, request):
        account = Account.objects.get(id=request.user.id)
        total_appointments_catered = Appointments.objects.filter(status='Completed', lab=account).count()

        seven_days_ago = datetime.now() - timedelta(days=7)
        completed_appointments_last_week = Appointments.objects.filter(
            status='Completed',
            date__gte=seven_days_ago,
        )
        total_staff_payment = completed_appointments_last_week.aggregate(Sum('payment__staff_payment'))['payment__staff_payment__sum']
        if total_staff_payment is not None:
            total_staff_payment_last_week = int(total_staff_payment // 100)
        else:
            total_staff_payment_last_week = 0

        total_appointments_today = Appointments.objects.filter(date=datetime.now(), lab=account).count()
        total_appointments_today_completed = Appointments.objects.filter(status='Completed', date=datetime.now(), lab=account).count()
        total_appointment_today_completed_perc = 0
        if total_appointments_today != 0:
            total_appointment_today_completed_perc = int((total_appointments_today_completed / total_appointments_today) * 100)

        data = {
            'total_appointments_catered': total_appointments_catered,
            'total_staff_payment_last_week': total_staff_payment_last_week,
            'total_appointments_today': total_appointments_today,
            'total_appointments_today_completed': total_appointments_today_completed,
            'total_appointment_today_completed_perc': total_appointment_today_completed_perc
        }
        # print('Data: ', data)
        return Response(data, status=status.HTTP_200_OK)

# Cancel an appointment by patient
class CancelAnAppointment(APIView):
    def delete(self, request):
        appointment_id = self.request.query_params.get('appointment_id', None)
        if not appointment_id:
            return Response({'error': 'Appointment ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        appointment = get_object_or_404(Appointments, appointment_id=appointment_id)

        appointment.status = 'Cancelled'
        appointment.save()
        try:
            appointment.payment.payment_status = 'cancelled'
            appointment.payment.save()
        except:
            return Response({'error': 'Payment error'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Appointment has been cancelled'}, status=status.HTTP_200_OK)
    

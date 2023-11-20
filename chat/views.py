from rest_framework.views import APIView
from .pusher import pusher_client
from rest_framework.response import Response
from django.db.models import OuterRef, Subquery
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q
from rest_framework import generics
from rest_framework import status
from django.shortcuts import get_object_or_404



from .models import ChatMessage
from authentication.models import Account
from .serializers import (
    MessageSerializer,
    FrontendMessageSerializer,
)
from appointments.models import Appointments



# Developed for Pusher. Not using anymore
class ChatAPI(APIView):
    def post(self, request):
        sender_email = request.data['senderEmail']
        recipient_email = request.data['recipientEmail']
        message_text = request.data['message']

        pusher_client.trigger('Remedy-development', 'message', {
            'email': sender_email,
            'message': message_text,
        })

        return Response(['Message recieved'])


class MyInbox(generics.ListAPIView):
    serializer_class = MessageSerializer
    
    def get_queryset(self):
        user_id = self.kwargs['user_id']

        messages = ChatMessage.objects.filter(
            id__in =  Subquery(
                Account.objects.filter(
                    Q(sender__reciever=user_id) |
                    Q(reciever__sender=user_id)
                ).distinct().annotate(
                    last_msg=Subquery(
                        ChatMessage.objects.filter(
                            Q(sender=OuterRef('id'),reciever=user_id) |
                            Q(reciever=OuterRef('id'),sender=user_id)
                        ).order_by('-id')[:1].values_list('id',flat=True) 
                    )
                ).values_list('last_msg', flat=True).order_by("-id")
            )
        ).order_by("-id")
            
        return messages


class GetMessages(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        sender_id = self.kwargs['sender_id']
        reciever_id = self.kwargs['reciever_id']
        messages =  ChatMessage.objects.filter(sender__in=[sender_id, reciever_id], reciever__in=[sender_id, reciever_id])
        return messages


class SendMessages(generics.CreateAPIView):
    queryset = ChatMessage.objects.all()
    serializer_class = FrontendMessageSerializer
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
class InitiateChatOnAppointment(generics.CreateAPIView):
    serializer_class = FrontendMessageSerializer

    def create(self, request, *args, **kwargs):
        appointment_id = request.data.get('appointmentId')
        print('Appointment ID: ', appointment_id)

        # Retrieve appointment details
        appointment = get_object_or_404(Appointments, appointment_id=appointment_id)
        if appointment.doctor:
            sender = appointment.doctor
        else:
            sender = appointment.lab
            
        patient = appointment.patient

        # Create message data
        message_data = {
            'sender': sender.id,
            'reciever': patient.id,
            'message': f'Message started for appointment: {appointment_id}',
            'is_read': False,
        }
        print('Message Data: ', message_data)

        # Create and save the chat message
        serializer = self.get_serializer(data=message_data)
        if not serializer.is_valid():
            print('Serializer Errors:', serializer.errors)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
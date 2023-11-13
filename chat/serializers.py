from rest_framework import serializers
from .models import ChatMessage
from authentication.models import Account

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = [ 'id',  'username',  'email', 'profile_pic_url' ]
    
    def __init__(self, *args, **kwargs):
        super(ProfileSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method=='POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3

class MessageSerializer(serializers.ModelSerializer):
    reciever_profile = ProfileSerializer(read_only=True)
    sender_profile = ProfileSerializer(read_only=True)

    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'reciever', 'reciever_profile', 'sender_profile', 'message', 'is_read', 'date']

    def __init__(self, *args, **kwargs):
        super(MessageSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method=='POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 2

class FrontendMessageSerializer(serializers.Serializer):
    sender = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    reciever = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    message = serializers.CharField()
    is_read = serializers.BooleanField()

    def create(self, validated_data):
        sender = validated_data.pop('sender')
        reciever = validated_data.pop('reciever')

        # Create ChatMessage instance
        return ChatMessage.objects.create(sender=sender, reciever=reciever, **validated_data)

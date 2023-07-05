import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.utils import timezone

class ChatConsumer(WebsocketConsumer):


    def connect(self):
        # accept connection
        self.user = self.scope['user']
        self.id = self.scope['url_route']['kwargs']['course_id']
        self.room_group_name = f'chat_{self.id}'
        
        # join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )
        
        self.accept()


    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name,self.channel_name)
        # receive message from WebSocket


    def receive(self, text_data):
        from .models import Chat
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.user
        now = timezone.now()
        # send message to WebSocket
        # send message to room group

        # store

        Chat.objects.create(user=user,created_at = now,updated_at = now,message=message)
        async_to_sync(self.channel_layer.group_send)(
        self.room_group_name,
        {
        'type': 'chat_message',
        'message': message,
        'user': user.username,
        'datetime': now.isoformat(),
        }
        )
        self.send(text_data=json.dumps({'message': message}))



    # receive message from room group
    def chat_message(self, event):
        # send message to WebSocket
        self.send(text_data=json.dumps(event))
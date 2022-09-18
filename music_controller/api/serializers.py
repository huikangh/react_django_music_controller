from rest_framework import serializers
from .models import Room

# translate a room and serialize it into a JSON response
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'code', 'host', 'guest_can_pause', 
                    'votes_to_skip', 'created_at')


# serializer handling the create room POST request
class CreateRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('guest_can_pause', "votes_to_skip")
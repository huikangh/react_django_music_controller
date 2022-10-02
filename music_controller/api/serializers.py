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


# serializer handling the update room quest
class UpdateRoomSerializer(serializers.ModelSerializer):
    # redefine the code field so the code field doesn't have to be unique
    code = serializers.CharField(validators=[])
    
    class Meta:
        model = Room
        fields = ('guest_can_pause', "votes_to_skip", "code")
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, status
from .serializers import RoomSerializer, CreateRoomSerializer
from .models import Room
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

# api view that allow us to view the list of rooms
class RoomView(generics.ListAPIView):
    # what we want to return
    queryset = Room.objects.all()
    # how to convert it into a different format
    serializer_class = RoomSerializer


# api view that allow us to create a new room
# APIView allows us to override default methods like GET and POST
class CreateRoomView(APIView):
    serializer_class = CreateRoomSerializer
    
    # overidding POST method
    def post(self, request, format=None):
        # check if current user has an active session in the server
        if not self.request.session.exists(self.request.session.session_key):
            # if not, create one for them
            self.request.session.create()

        # takes in request data and serialize it into python representation
        # in this case, it will takes in "guest_can_pause" and "votes_to_skip"
        serializer = self.serializer_class(data=request.data)
        # if the request data is valid
        if serializer.is_valid():
            # retrieve all the necessary data to create a Room
            guest_can_pause = serializer.data.get("guest_can_pause")
            votes_to_skip = serializer.data.get("votes_to_skip")
            host = self.request.session.session_key
            # retrieve the list of rooms the current user is hosting from the database model Room
            queryset = Room.objects.filter(host=host)
            # if a room already exist, update the room
            if queryset.exists():
                room = queryset[0]
                room.guest_can_pause = guest_can_pause
                room.votes_to_skip = votes_to_skip
                room.save(update_fields=['guest_can_pause', 'votes_to_skip'])
                return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
            # if no room, create a new one
            else:
                room = Room(host=host, guest_can_pause=guest_can_pause, votes_to_skip=votes_to_skip)
                room.save()
                return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)
            
        # if the request data is invalid, return a bad request response 400
        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, status
from .serializers import RoomSerializer, CreateRoomSerializer
from .models import Room
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse

# Create your views here.

# api view that allow us to view the list of rooms
class RoomView(generics.ListAPIView):
    # what we want to return
    queryset = Room.objects.all()
    # how to convert it into a different format
    serializer_class = RoomSerializer



# api view that handle requests for a room's data based on room code
class GetRoom(APIView):
    serializer_class = RoomSerializer
    lookup_url_kwarg = 'code'

    def get(self, request, format=None):
        # look for the code from the url
        code = request.GET.get(self.lookup_url_kwarg)
        if code != None:
            # find the room with the specified code
            room = Room.objects.filter(code=code)
            if len(room) > 0:
                # extract the room data
                data = RoomSerializer(room[0]).data
                # update the room data
                data['is_host'] = self.request.session.session_key == room[0].host
                # return room data
                return Response(data, status=status.HTTP_200_OK)
            return Response({"Room Not Found": "Invalid Room Code."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"Bad Request": "Code parameter not found in request"}, status=status.HTTP_400_BAD_REQUEST)



# api view that takes in a room code from user to join a room
class JoinRoom(APIView):
    lookup_url_kwarg = 'code'

    def post(self, request, format=None):
        # check if current user has an active session in the server
        if not self.request.session.exists(self.request.session.session_key):
            # if not, create one for them
            self.request.session.create()

        # look for the room code from the POST request data
        code = request.data.get(self.lookup_url_kwarg)
        if code != None:
            # find the room the user is looking for
            room_result = Room.objects.filter(code=code)
            if len(room_result) > 0:
                room = room_result[0]
                # make a note that this user is in this room
                # create a temporary storage object "room_code":code in the user session
                self.request.session['room_code'] = code
                return Response({'message': 'Room Joined!'}, status=status.HTTP_200_OK)
            return Response({'Bad Request': 'Invalid Room Code'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'Bad Request': 'Invalid post data, did not find a code key'}, status=status.HTTP_400_BAD_REQUEST)



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
                self.request.session['room_code'] = room.code
                return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
            # if no room, create a new one
            else:
                room = Room(host=host, guest_can_pause=guest_can_pause, votes_to_skip=votes_to_skip)
                room.save()
                self.request.session['room_code'] = room.code
                return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)
            
        # if the request data is invalid, return a bad request response 400
        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)


# api view that handles a GET request to check if the current user is already in a room
class UserInRoom(APIView):
    def get(self, request, format=None):
        # check if current user has an active session in the server
        if not self.request.session.exists(self.request.session.session_key):
            # if not, create one for them
            self.request.session.create()
        # create an ojbect containing the user's existing room_code
        data = {
            'code': self.request.session.get('room_code')
        }
        # JsonResponse takes a pyhton dictionary and serialize it into a json object
        return JsonResponse(data, status=status.HTTP_200_OK)
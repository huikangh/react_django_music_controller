from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics
from .serializers import RoomSerializer
from .models import Room

# Create your views here.

# api view that allow us to view the list of rooms
class RoomView(generics.ListAPIView):
    # what we want to return
    queryset = Room.objects.all()
    # how to convert it into a different format
    serializer_class = RoomSerializer


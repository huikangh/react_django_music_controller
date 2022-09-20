from django.urls import path 
from .views import GetRoom, RoomView, CreateRoomView

# import functions from views.py
# and call those functions according to the url patern
urlpatterns = [
    path('room', RoomView.as_view()),
    path('create-room', CreateRoomView.as_view()),
    path('get-room', GetRoom.as_view()),
]
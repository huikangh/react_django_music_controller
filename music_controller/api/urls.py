from django.urls import path 
from .views import RoomView

# import functions from views.py
# and call those functions according to the url patern
urlpatterns = [
    path('room', RoomView.as_view())
]
from django.urls import path
from .views import index

# django needs to know that this urls.py file belongs to the frontend app
app_name = "frontend"

urlpatterns = [
    path('', index, name=""),
    path('info', index),
    path('join', index),
    path('create', index),
    path('room/<str:roomCode>', index)
]

from django.urls import path 
from .views import main

# import functions from views.py
# and call those functions according to the url patern
urlpatterns = [
    path('', main)
]
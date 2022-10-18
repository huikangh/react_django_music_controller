from django.db import models
import string
import random

def generate_unique_code():
    length = 6
    while True:
        # generate a random list of upper case letters of length k
        letters = random.choices(string.ascii_uppercase, k=length)
        # turn the list into a string to be our code
        code = ''.join(random.choices(string.ascii_uppercase, k=length))
        # check whether the code already exist
        # if not, break the while loop and return code
        if Room.objects.filter(code=code).count() == 0:
            break
    return code


# Create your models here.
class Room(models.Model):
    code = models.CharField(max_length=8, default=generate_unique_code, unique=True)
    host = models.CharField(max_length=50, unique=True)
    guest_can_pause = models.BooleanField(null=False, default=False)
    votes_to_skip = models.IntegerField(null=False, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    current_song = models.CharField(max_length=50, null=True)


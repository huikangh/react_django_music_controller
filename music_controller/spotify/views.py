from django.shortcuts import render, redirect
from .credentials import REDIRECT_URI, CLIENT_SECRET, CLIENT_ID
from rest_framework.views import APIView
from requests import Request, post
from rest_framework import status
from rest_framework.response import Response
from .util import *
from api.models import Room
from .models import Vote


# view that returns an URL that we can use to Authenticate the Spotify application
class AuthURL(APIView):
    def get(self, request, format=None):
        # specifies what information we want to access from spotify
        scopes = 'user-read-playback-state user-modify-playback-state user-read-currently-playing'
        # this generates an url for us
        url = Request('GET', 'https://accounts.spotify.com/authorize', params={
            'scope': scopes,
            'response_type': 'code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID
        }).prepare().url

        return Response({'url': url}, status=status.HTTP_200_OK)



# callback function that send another request to Spotify API to get access and refresh tokens
# after user log in and authenticate their acess
def spotify_callback(request, format=None):
    # code to authenitcate user
    code = request.GET.get('code')
    error = request.GET.get('error')

    # send a request to Spotify API to get access and refresh tokens
    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()
    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    error = response.get('error')
    # store the user information into the SpotifyToken model
    if not request.session.exists(request.session.session_key):
        request.session.create()
    update_or_create_user_tokens(
        request.session.session_key, access_token, token_type, expires_in, refresh_token)
    # redirect back to original application (to the HomePage of frontend app)
    return redirect('frontend:')



# view that tells us whether the user is authenticated
class IsAuthenticated(APIView):
    def get(self, request, format=None):
        is_authenticated = is_spotify_authenticated(self.request.session.session_key)
        return Response({'status': is_authenticated}, status=status.HTTP_200_OK)



# view that sends another HTTP request to Spotify to retreive current song info
class CurrentSong(APIView):
    def get(self, request, format=None):
        # get the room info, and the host of the room
        room_code = self.request.session.get('room_code')
        room = Room.objects.filter(code=room_code)
        if room.exists():
            room = room[0]
        else:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        host = room.host
        # create and send http request url to spotify
        endpoint = "player/currently-playing"
        response = execute_spotify_api_request(host, endpoint)
        # parse only the needed info from the response
        if 'error' in response or 'item' not in response:
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        item = response.get('item')
        duration = item.get('duration_ms')
        progress = response.get('progress_ms')
        album_cover = item.get('album').get('images')[0].get('url')
        is_playing = response.get('is_playing')
        song_id = item.get('id')

        artist_string = ""
        for i, artist in enumerate(item.get('artists')):
            if i > 0:
                artist_string += ", "
            name = artist.get('name')
            artist_string += name
        votes = len(Vote.objects.filter(room=room, song_id=song_id))

        # combine all the needed info into an object
        song = {
            'title': item.get('name'),
            'artist': artist_string,
            'duration': duration,
            'time': progress,
            'image_url': album_cover,
            'is_playing': is_playing,
            'votes': votes,
            'votes_required': room.votes_to_skip,
            'id': song_id
        }
        self.update_room_song(room, song_id)
        return Response(song, status=status.HTTP_200_OK)

    # helper function that updates the current song of a certain room
    def update_room_song(self, room, song_id):
        current_song = room.current_song
        if current_song != song_id:
            room.current_song = song_id
            room.save(update_fields=['current_song'])
            # delete all vote objects when we switch to a new song
            votes = Vote.objects.filter(room=room).delete()



# view that sends another HTTP request to Spotify to pause current song
class PauseSong(APIView):
    def put(self, response, format=None):
        room_code = self.request.session.get('room_code')
        room = Room.objects.filter(code=room_code)[0]
        if self.request.session.session_key == room.host or room.guest_can_pause:
            pause_song(room.host)
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        return Response({}, status=status.HTTP_403_FORBIDDEN)



# view that sends another HTTP request to Spotify to play current song
class PlaySong(APIView):
    def put(self, response, format=None):
        room_code = self.request.session.get('room_code')
        room = Room.objects.filter(code=room_code)[0]
        if self.request.session.session_key == room.host or room.guest_can_pause:
            play_song(room.host)
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        return Response({}, status=status.HTTP_403_FORBIDDEN)



class SkipSong(APIView):
    def post(self, request, format=None):
        # get the Room object of current room
        room_code = self.request.session.get('room_code')
        room = Room.objects.filter(code=room_code)[0]
        votes_needed = room.votes_to_skip
        # skip song if user is the host
        if self.request.session.session_key == room.host:
            # delete all the votes for the current song then skip
            Vote.objects.filter(room=room, song_id=room.current_song).delete()
            skip_song(room.host)
        # if not, create a Vote object for the current vote
        else:
            Vote(user=self.request.session.session_key, room=room, song_id=room.current_song).save()
            # then check whether there are enough votes
            votes = Vote.objects.filter(room=room, song_id=room.current_song)
            if len(votes) >= votes_needed:
                votes.delete()
                skip_song(room.host) 

        return Response({}, status.HTTP_204_NO_CONTENT)
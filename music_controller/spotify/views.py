from django.shortcuts import render, redirect
from .credentials import REDIRECT_URI, CLIENT_SECRET, CLIENT_ID
from rest_framework.views import APIView
from requests import Request, post
from rest_framework import status
from rest_framework.response import Response
from .util import update_or_create_user_tokens, is_spotify_authenticated

# view that returns an URL that we can use to Authenticate the Spotify application
class AuthURL(APIView):
    def get(self, request, format=None):
        # specifies what information we want to access from spotify
        scopes = 'user-read-playback-state user-modify-playback-state user-read-currently-playing'
        # this generates an url for us
        url = Request('GET', 'https://accounts.spotify.com/authorize', params={
            'scopes': scopes,
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
from .models import SpotifyToken
from django.utils import timezone
from datetime import timedelta
from .credentials import CLIENT_ID, CLIENT_SECRET
from requests import post, put, get


BASE_URL = "https://api.spotify.com/v1/me/"

# retrieves all user tokens in the SpotifyToken model with matching user/session_id
def get_user_tokens(session_id):
    user_tokens = SpotifyToken.objects.filter(user=session_id)
    if user_tokens.exists():
        return user_tokens[0]
    else:
        return None


# saves user tokens into our SpotifyToken model
def update_or_create_user_tokens(session_id, access_token, token_type, expires_in, refresh_token):
    # check if user has any exisiting tokens
    tokens = get_user_tokens(session_id)
    # calculate the expire time
    expires_in = timezone.now() + timedelta(seconds=expires_in)
    # update/create user token in the SpotifyToken model
    if tokens:
        tokens.access_token = access_token
        tokens.refresh_token = refresh_token
        tokens.expires_in = expires_in
        tokens.token_type = token_type
        tokens.save(update_fields=['access_token', 'refresh_token', 'expires_in', 'token_type'])
    else:
        tokens = SpotifyToken(
            user=session_id,
            access_token=access_token,
            refresh_token=refresh_token,
            token_type=token_type,
            expires_in=expires_in)
        tokens.save()


# function that checks if the user is still authenticated
def is_spotify_authenticated(session_id):
    tokens = get_user_tokens(session_id)
    if tokens:
        # check whether the user tokens are expired
        expiry = tokens.expires_in
        # if expired, refresh the tokens
        if expiry <= timezone.now():
            refresh_spotify_token(session_id)
        return True
    return False


# send a POST request to Spotify API to refresh token
def refresh_spotify_token(session_id):
    refresh_token = get_user_tokens(session_id).refresh_token
    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()
    # response now should contain the new access_token and refresh_token
    access_token = response.get('access_token')
    token_type = response.get('token_type')
    expires_in = response.get('expires_in')
    # refresh_token = response.get('refresh_token')
    # update the user token model with the new tokens
    update_or_create_user_tokens(session_id, access_token, token_type, expires_in, refresh_token)


# helper function that sends request to spotify api with user tokens
def execute_spotify_api_request(session_id, endpoint, post_=False, put_=False):
    tokens = get_user_tokens(session_id)
    headers = {'Content-Type': 'application/json', 'Authorization': "Bearer " + tokens.access_token}
    if post_:
        post(BASE_URL + endpoint, headers=headers)
    if put_:
        put(BASE_URL + endpoint, headers=headers)
    # empty dictionary because of the get request syntax
    response = get(BASE_URL + endpoint, {}, headers=headers)
    try:
        return response.json()
    except:
        return {'Error': 'Issue with request'}


# function that calls the helper function to sends a play song request to spotify api
def play_song(session_id):
    return execute_spotify_api_request(session_id, "player/play", put_=True)


# function that calls the helper function to sends a pause song request to spotify api
def pause_song(session_id):
    return execute_spotify_api_request(session_id, "player/pause", put_=True)  


# function that calls the helper function to sends a next song request to spotify api
def skip_song(session_id):
    return execute_spotify_api_request(session_id, "player/next", post_=True)
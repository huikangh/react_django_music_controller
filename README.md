## React & Django Project Change log

#### Part#2

- created a Room model in models.py with fields code, host, guest_can_pause, votes_to_skip, and created_at
- created the serializers.py file and a RoomSerializer class that translate the Room model into JSON format with desired fields
- created a RoomView class in views.py that allows us to view the list of Rooms and/or add a new Room depending on which rest_framework generics we use

#### Part#3

- created a frontend app with folder for all the javascript/react files
- the idea is to have django application render a template, then the react code would take over and fill it in
- installed webpack, babel, react,react-dom, react-router-dom, material-ui, material-ui-icons using npm
- added script file, babel.config.json, which converts codes into codes that would in older browsers, and to use async/await
- added script file, webpack.config.js, which bundles all javascript into one file and server to browser
- set up url endpoint in music_controller/urls.py so a blank url would be route to frontend/urls.py, which then a blank url again would route to the "index" view
- when we run the webpack script with "npm run dev", the script looks at index.js file, bundles all the js files together as one "main.js" in the frontend folder, the file would then be rendered as the frontend "index" view

#### Part#4

- Created different react components for different pages: HomePage, CreateRoomPage, RoomJoinPage
- utilized react router in HomePage to route to different components (CreatRoomPage & RoomJoinPage) with assigned paths
- in order to actually set up the routing, we have to add the routes in both Django (in frontend/urls.py) and React (HomePage.js)

#### Part#5

- added a backend view, CreateRoomView, that allow us to create a new room by taking in POST requests to the end point we set up
- the CreateRoomView utilized/inherited rest_framework.APIView class to override the POST method so we can control how we handle the POST requests that are sent to this view
- to create/update a room, the view extracts information from the user's POST request such as guest_can_pause, votes_to_skip, and even the session key, provided by the user at the frontend
- whenever we connect to a website, we would establish a session, this allows the website to maintain our state when we revisit (ex. we don't have to re-login)
- our backend server will stores and identifies user by their sessions

#### Part#6

- added more react jsx and html/css code, such as radio buttons, text fields, and buttons in frontend/components/CreateRoomPage.js to style the frontend webpage
- added react states, guestCanPause and votesToSkip, in CreateRoomPage to keep track of the information entered by the user
- added functions, handleVotesChange(), handleGuestCanPauseChange(), and handleRoomButtonPressed() that handle different events in CreateRoomPage
- specifically, handleRoomButtonPressed() gathered all the user entered information from the component states, and send a POST request to the api/create-room backend endpoint to create a room in the server

#### Part#7

- added Room.js that allows us to view specific rooms
- added a backend view, GetRoom, that allows frontend to fetch for the room data based on the room code
- send up endpoint for the backedn view, GetRoom, with the pattern "room/:roomCode" where any string after the "room/" pattern will be processed as the room code
- Room.js will send a GET request to the api/get-room endpoint with the room code, which then the GetRoom view would process the room code in the url and return the room data back, then Room.js utilizes the returned response and fill up the page with the room's data
- edited CreateRoomPage.js so upon creating a new room, the webpage will navigate to the newly created room page

#### Part#8

- edited index.css to center the app class
- added a backend view, JoinRoom, that allows the frontend user to fetch for existing room to join nased on the room code
- added more react jsx and html/css code, such as textfield and buttons in frontend/components/JoinRoomPage.js to style the frontend webpage
- added react states and functions in JoinRoomPage.js to keep track of the information entered by the user and handle user actions like a button click
- specifically, roomButtonPressed() in JoinRoomPage gathered the user entered room code from the component state, and send a POST request to the api/join-room backend endpoint to find and join the existing room

#### Part#9

- styled the HomePage by adding a renderHomePage() that includes a button to direct to JoinRoomPage and a button to direct to CreateRoomPage
- right when the homepage load, we need to check if the user is already in a room, and then redirect to that room page
- added a backend view, UserInRoom, that allows the frontend to check whether the current user is already in an existing room. If yes, the view would return the room code
- added a frontend function at HomePage that fetch goes to the UserInRoom view to check whether user already in a room. If yes, frontend would update the roomCode state, and HomePage would be directed to RoomPage instead

#### Part#10

- styled the RoomPage by using Typography and adding a back button to leave the RoomPage
- added a function, leaveButtonPressed(), in Room.js that sends a POST request to the backend to leave the room when the button is pressed. When the request is done, the room_code state in HomePage.js will be reset and the user will be redirected to the HomePage
- added a backend view, LeaveRoom, that allows the user to leave the current room by removing the room_code stored in the user's session. If the user is also the host, the room would also be deleted

#### Part#11

- added a backend view, UpdateRoom, that allows the host of a room to update room settings by taking in a room code and the new settings for the room, then updates the setting of the room in the backend model/database
- added a Settings button in Room.js that shows up only if the user is the host of the room
- added a boolean state in Room.js, showSettings, that determines whether or not to render the Settings page
- added a component that is reusing the CreateRoomPage component in Room.js to render the Settings page when the host clicks on the Settings button

#### Part#12

- added functions, renderCreateButtons() and renderUpdateButtons(), in CreateRoomPage.js that renders different frontend interface depending on whether we are creating a room or updating a room
- added function, handleUpdateButtonPressed(), in CreateRoomPage.js that handles the update room button and sends a PATCH request to a backend endpoint to update the backend database with the new room settings
- after we updated the new room settings in the backend database, when we go back to the room and, the Room component would be re-rendered and the component would fetches for the room data and it will be retrieving the updated room data
- added a feature using the imported Collapse and Alert components to display an alert message when the user updates room settings

#### Part#13

- created an application on Spotify Developer
- created a new django project named spotify that handles all the interaction with the spotify API
- added a view in spotify/views.py, AuthURL(), to handle frontend request to generate an authenticate url to the Spotify API
- added a view in spotify/views.py, spotify_callback(), that act as a callback function that send another request to Spotify API to get access and refresh tokens after user log in and authenticate their acess
- added a model in spotify/models.py to store all the user information we got from requesting the Spotify API (refresh_token, access_token, token_type, etc)
- added a util.py file in /spotify that contains utility functions: get_user_tokens(), update_or_create_user_tokens(), is_spotify_authenticated(), refresh_spotify_token(), that interacts with the database model SpotifyToken
- added a view in spotify/views.py, IsAuthenticated(), to handle frontend request to verify whether the user is authenticated by calling the util.py function is_spotify_authenticate()
- added a function, authenticateSpotify(), in frontend/Room.js that would get called whenever a user joins a room and the user is the host of the room. The function will send a request to the app's backend to check whether the user is logged in. If not, the backend would send back a Spotify authentication url to be redirected to the Spotify page to log in. After user logs in, spotify_callback() will be called

#### Part#14

- added function execute_spotify_api_request() in spotify/util.py that send another request to the Spotify API
- added view CurrentSong() in spotify/views.py that handles requests to send another request to the Spotify API by calling execute_spotify_api_request() to get the current song information, the view will return a custom song object containing all the needed information
- added function, getCurrentSong(), in Room.js that sends an HTTP request to our backend endpoint to fetch for current song info
- added new state, song, in Room.js that is an object storing all the needed information of the current playing song
- added new React component, MusicPlayer.js, that takes in the song state with all the needed song info and renders a nice music player component

#### Part#15

- added functions pauseSong() and playSong() in MusicPlayer.js that handles frontend button press to play or pause the song by sending requests to our backend
- added two url endpoints in spotify/urls.py, "pause" and "play" to handle frontend requests and route them to the corresponding views
- added views PauseSong() and PlaySong() in spotify/views.py that handles play/pause song requests from the frontend calling either pause_song() or play_song() to pause or play the current song
- added functions pause_song() and play_song() in spotify/util.py that calls the helper function execute_spotify_api_request() to send request the the Spotify API to play or pause the current song

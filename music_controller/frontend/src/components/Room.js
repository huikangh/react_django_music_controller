import React, { useState, useEffect} from "react";
import { useParams, useNavigate } from "react-router-dom"; 
import { Grid, Button, Typography } from "@material-ui/core";
import CreateRoomPage from "./CreateRoomPage";
import MusicPlayer from "./MusicPlayer";

export default function Room(props) {
    
    const [votesToSkip, setVotesToSkip] = useState(2);
    const [guestCanPause, setGuestCanPause] = useState(false);
    const [isHost, setIsHost] = useState(false);
    const [showSettings, setShowSettings] = useState(false);
    const [spotifyAuthenticated, setSpotifyAuthenticated] = useState(false);
    const [song, setSong] = useState({});

    const navigate = useNavigate();
    
    // useParams() gets all parameters from the current URL matched by the route path
    const { roomCode } = useParams();

    // GET request to backend to fetch for current song info
    // then update the song state
    function getCurrentSong() {
        fetch('/spotify/current-song')
            .then((response) => {
                if (!response.ok) {
                    return {};
                } else {
                    return response.json();
                }
            })
            .then((data) => {
                setSong(data);
                console.log(data);
            });
    }

    // POST request to leave the current room
    function leaveButtonPressed() {
        const requestOptions = {
            method: "POST",
            headers: { "Content-Type": "application/json" },
        }
        fetch('/api/leave-room', requestOptions)
            .then((response) => {
                props.leaveRoomCallback();
                navigate("/");
            }
        )
    }

    function updateShowSettings(value) {
        setShowSettings(value)
    }

    function renderSettings() {
        return (
            <Grid container spacing={1}>

                <Grid item xs={12} align="center">
                    <CreateRoomPage 
                        update={true} 
                        votesToSkip={votesToSkip} 
                        guestCanPause={guestCanPause} 
                        roomCode={roomCode}
                        // updateCallback={} 
                    />
                </Grid>

                <Grid item xs={12} align="center">
                    <Button variant="contained" color="secondary" onClick={()=>updateShowSettings(false)}>
                        Close
                    </Button>
                </Grid>

            </Grid>
        )
    }

    // only render Settings button if user is the host
    function renderSettingsButton() {
        return (
            <Grid item xs={12} align="center">
                <Button variant="contained" color="primary" onClick={() => updateShowSettings(true)}>
                    Settings
                </Button>
            </Grid>
        );
    }

    // send request to backend to check whether current user is authenticated
    function authenticateSpotify() {
        // first check if user is authenticated
        fetch('/spotify/is-authenticated')
        .then((response) => response.json())
        .then((data) => {
            setSpotifyAuthenticated(data.status)
            // if user is not authenticated, redirect user to Spotify authentication page
            if (!data.status) {
                fetch('/spotify/get-auth-url')
                .then((response) => response.json())
                .then((data) => {
                    window.location.replace(data.url);
                })
            }
        })
    }


    // send a GET request to /api/get-room to fetch for room data using the roomcCode
    function getRoomDetails() {
        fetch('/api/get-room' + '?code=' + roomCode)
                .then((response) => {
                    // if no room, reset the roomCode state and redirect to home page
                    if (!response.ok) {
                        props.leaveRoomCallback();
                        navigate("/");
                    }
                    return response.json()
                })
                .then((data) => {
                    setVotesToSkip(data.votes_to_skip)
                    setGuestCanPause(data.guest_can_pause)
                    setIsHost(data.is_host)
                    if (isHost) {
                        authenticateSpotify();
                    }
                })
    }

    // fetch for room info everytime the Room page is rendered
    getRoomDetails();
    // fetch for song info every 1 second
    useEffect(()=> {
        setTimeout(()=>{
            getCurrentSong();
           }, 1000)
    }, [song])


    // if showSettings is true, render the Settings component instead
    if (showSettings) {
        return renderSettings();
    }

    return (
        <Grid container spacing={1}>

            <Grid item xs={12} align="center">
                <Typography variant="h4" component="h4">
                    Code: {roomCode}
                </Typography>
            </Grid>

            {/* <Grid item xs={12} align="center">
                <Typography variant="h6" component="h6">
                    Votes: {votesToSkip}
                </Typography>
            </Grid>

            <Grid item xs={12} align="center">
                <Typography variant="h6" component="h6">
                    Guest Can Pause: {String(guestCanPause)}
                </Typography>
            </Grid>

            <Grid item xs={12} align="center">
                <Typography variant="h6" component="h6">
                    Host: {String(isHost)}
                </Typography>
            </Grid> */}

            <MusicPlayer {...song} />

            {isHost ? renderSettingsButton() : null}

            <Grid item xs={12} align="center">
                <Button variant="contained" color="secondary" onClick={leaveButtonPressed}>
                    Leave Room
                </Button>
            </Grid>

        </Grid>
    )
}

import React, { useState } from "react";
import { useParams, useNavigate } from "react-router-dom"; 
import { Grid, Button, Typography } from "@material-ui/core";

export default function Room(props) {
    
    const[votesToSkip, setVotesToSkip] = useState(2);
    const[guestCanPause, setGuestCanPause] = useState(false);
    const[isHost, setIsHost] = useState(false);

    const navigate = useNavigate();
    
    // useParams() gets all parameters from the current URL matched by the route path
    const { roomCode } = useParams();

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

    // send a GET request to /api/get-room to fetch for room data using the roomcCode
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
            })

    return (

        <Grid container spacing={1}>

            <Grid item xs={12} align="center">
                <Typography variant="h4" component="h4">
                    Code: {roomCode}
                </Typography>
            </Grid>

            <Grid item xs={12} align="center">
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
            </Grid>

            <Grid item xs={12} align="center">
                <Button variant="contained" color="secondary" onClick={leaveButtonPressed}>
                    Leave Room
                </Button>
            </Grid>

        </Grid>
    )
}

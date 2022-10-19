import React, { useState, useEffect } from 'react';
import { Grid, Button, Typography, IconButton } from "@material-ui/core";
import NavigateBeforeIcon from "@material-ui/icons/NavigateBefore";
import NavigateNextIcon from "@material-ui/icons/NavigateNext";
import { Link } from "react-router-dom";


const pages = {
    JOIN: "pages.join",
    CREATE: "pages.create",
}


export default function Info(props) {

    const [page, setPage] = useState(pages.JOIN);

    function joinInfo() {
        return (
            <div>
                <br/>
                <Typography variant="body1">
                    Join a Room
                </Typography>
                <Typography variant="body2">
                    Joining a room allows a user to join an existing room by entering the room code. Inside a room, users would have access to the Spotify music controller.
                </Typography>
            </div>
        );
    }

    function createInfo() {
        return (
            <div>
                <br/>
                <Typography variant="body1">
                    Create a Room
                </Typography>
                <Typography variant="body2">
                    Creating a room allows a user to create a new room. The user will also become the host of the room with the ability to configure the settings for the room.
                </Typography>
            </div>
        );
    }

    return (
        <Grid container spacing={1}>

            <Grid item xs={12} align="center">
                <Typography component="h4" variant="h4">
                    What is House Party?
                </Typography>
            </Grid>

            <Grid item xs={12} align="center">
                <Typography variant="body2">
                    House Party is a web application that allows users to create and join rooms and control a Spotify music player.
                </Typography>
            </Grid>

            <Grid item xs={12} align="center">
                <Typography variant="body1">
                    { page === pages.JOIN ? joinInfo() : createInfo() }
                </Typography>
            </Grid>

            <Grid item xs={12} align="center">
                <IconButton onClick={() => {page === pages.CREATE ? setPage(pages.JOIN) : setPage(pages.CREATE)}}>
                { page === pages.JOIN ? <NavigateNextIcon /> : <NavigateBeforeIcon /> }
                </IconButton>
            </Grid>

            <Grid item xs={12} align="center">
                <Button color="secondary" variant="contained" to="/" component={Link}> 
                    Back
                </Button>
            </Grid>

        </Grid>
    )
}
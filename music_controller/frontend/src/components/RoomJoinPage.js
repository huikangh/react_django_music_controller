import React, { useState } from "react"
import { useNavigate } from "react-router-dom"
import { TextField, Button, Grid, Typography } from "@material-ui/core"
import { Link } from "react-router-dom"

export default function RoomJoinPage() {

    let navigate = useNavigate();

    const [roomCode, setRoomCode] = useState("")
    const [error, setError] = useState("")

    function handleTextFieldChange(e) {
        setRoomCode(e.target.value)
    }

    // set a POST request with the room code in a JSON format to the backend end point
    function roomButtonPressed() {
        const requestOptions = {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                code: roomCode
            })
        };
        fetch('api/join-room', requestOptions)
            .then((response) => {
                if (response.ok) {
                    navigate(`/room/${roomCode}`)
                } else {
                    setError("Room not found.")
                }
            })
            .catch((error) => console.log(error))
    }

    return (
        <Grid container spacing={1} alignItems="center" direction="column">

            <Grid item xs={12}>
                <Typography variant="h4" component="h4">
                    Join a Room
                </Typography>
            </Grid>

            <Grid item xs={12}>
                <TextField
                    error={error}
                    label="Code"
                    placeholder="Enter a Room Code"
                    value={roomCode}
                    helperText={error}
                    variant="outlined"
                    onChange={handleTextFieldChange}
                />
            </Grid>

            <Grid item xs={12}>
                <Button variant="contained" color="primary" onClick={roomButtonPressed} >Enter Room</Button>
            </Grid>

            <Grid item xs={12}>
                <Button variant="contained" color="secondary" to="/" component={Link}>Back</Button>
            </Grid>

        </Grid>
    )

}
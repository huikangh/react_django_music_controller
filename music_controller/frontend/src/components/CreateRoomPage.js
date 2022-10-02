import React, { useState } from "react";
import { useNavigate } from 'react-router-dom';
import Button from "@material-ui/core/Button"
import Grid from "@material-ui/core/Grid"
import Typography from "@material-ui/core/Typography"
import TextField from "@material-ui/core/TextField"
import FormHelperText from "@material-ui/core/FormHelperText"
import FormControl from "@material-ui/core/FormControl"
import { Link } from "react-router-dom"
import Radio from "@material-ui/core/Radio"
import RadioGroup from "@material-ui/core/RadioGroup"
import FormControlLabel from "@material-ui/core/FormControlLabel"
import { Collapse } from "@material-ui/core"
import Alert from "@material-ui/lab/Alert"

// value of props could be empty if we didn't pass in any values when rendering the component
// we can define default values to props with this syntax
CreateRoomPage.defaultProps = {
    votesToSkip: 2,
    guestCanPause: true,
    update:false,
    roomCode: null,
    updateCallback: () => {},
}

export default function CreateRoomPage(props) {

    let navigate = useNavigate();
    const [guestCanPause, setGuestCanPause] = useState(props.guestCanPause)
    const [votesToSkip, setVotesToSkip] = useState(props.votesToSkip)
    const [successMsg, setSuccessMsg] = useState("")
    const [errorMsg, setErrorMsg] = useState("")

    // get value from the votes textfield and update the state
    function handleVotesChange(event) {
        setVotesToSkip(event.target.value)
    }

    // get value from the radio group and update the state
    function handleGuestCanPauseChange(event) {
        setGuestCanPause(event.target.value === "true" ? true : false)
    }

    // send a POST request with the state values in a JSON format to the backend end point
    function handleRoomButtonPressed() {
        const requestOptions = {
            method: "POST",
            headers: {'Content-Type': 'application/json' },
            body: JSON.stringify({
                votes_to_skip: votesToSkip,
                guest_can_pause: guestCanPause,
            }),
        };
        fetch("/api/create-room", requestOptions)
            .then((response) => response.json())
            .then((data) => navigate('/room/' + data.code));
    }
    
    // send a PATCH request with the updated state values in a JSON format to the backend end point
    function handleUpdateButtonPressed() {
        const requestOptions = {
            method: "PATCH",
            headers: {'Content-Type': 'application/json' },
            body: JSON.stringify({
                votes_to_skip: votesToSkip,
                guest_can_pause: guestCanPause,
                code: props.roomCode
            }),
        };
        fetch("/api/update-room", requestOptions)
            .then((response) => {
                if (response.ok) {
                    setSuccessMsg("Room updated successfully!")
                } else {
                    setErrorMsg("Error updating room...")
                }
            })
    }

    // renders the appropriate buttons when the page is "Creating a Room"
    function renderCreateButtons() {
        return (
            <Grid container spacing={1}>
                <Grid item xs={12} align="center">
                    <Button color="primary" variant="contained" onClick={handleRoomButtonPressed}>
                        Create A Room
                    </Button>
                </Grid>

                <Grid item xs={12} align="center">
                    <Button color="secondary" variant="contained" to="/" component={Link} >
                        Back
                    </Button>
                </Grid>
            </Grid>
        )
    }

    // renders the appropriate buttons when the page is "Update Room"
    function renderUpdateButtons() {
        return (
            <Grid item xs={12} align="center">
                <Button color="primary" variant="contained" onClick={handleUpdateButtonPressed}>
                    Update Room
                </Button>
            </Grid>
        )
    }


    const title = props.update ? "Update Room" : "Create a Room"

    // 12 is the maximum number for the width of grid
    return (
        <Grid container spacing={1}>

<           Grid item xs={12} align="center">
                <Collapse in={errorMsg != "" || successMsg != ""}>
                    { successMsg != "" ? 
                    (<Alert 
                        severity="success" 
                        onClose={()=>setSuccessMsg("")}>
                        {successMsg} 
                    </Alert>) : 
                    (<Alert 
                        severity="success"
                        onClose={()=>setErrorMsg("")}>
                        {errorMsg}
                    </Alert>) }
                </Collapse>
            </Grid>

            <Grid item xs={12} align="center">
                <Typography component='h4' variant='h4'>
                    {title}
                </Typography>
            </Grid>

            <Grid item xs={12} align="center">
                <FormControl component="fieldset">
                    <FormHelperText>
                        <div align="center">Guest Control of Playback State</div> 
                    </FormHelperText>
                    <RadioGroup row defaultValue={props.guestCanPause.toString()} onChange={handleGuestCanPauseChange}>
                        <FormControlLabel
                            value="true" 
                            control={<Radio color="primary" />} 
                            label="Play/Pause" 
                            labelPlacement="bottom" />
                        <FormControlLabel
                            value="false" 
                            control={<Radio color="secondary" />} 
                            label="No Control" 
                            labelPlacement="bottom" />
                    </RadioGroup>
                </FormControl>
            </Grid>

            <Grid item xs={12} align="center">
                <FormControl>
                    <TextField 
                        required={true} 
                        type="number"
                        onChange={handleVotesChange}
                        defaultValue={votesToSkip} 
                        inputPros={{ min:1, style: {textAlign: "center"} }}/>
                    <FormHelperText>
                        <div align="center"> Votes Required to Skip Song</div>
                    </FormHelperText>
                </FormControl>
            </Grid>

            {props.update ? renderUpdateButtons() : renderCreateButtons()}

        </Grid>
    );
}
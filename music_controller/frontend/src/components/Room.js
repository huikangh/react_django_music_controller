import React, { useState } from "react";
import { useParams } from "react-router-dom";  


export default function Room(props) {
    
    const[votesToSkip, setVotesToSkip] = useState(2);
    const[guestCanPause, setGuestCanPause] = useState(false);
    const[isHost, setIsHost] = useState(false);
    
    // useParams() gets all parameters from the current URL matched by the route path
    const { roomCode } = useParams();

    // send a GET request to /api/get-room to fetch for room data using the roomcCode
    fetch('/api/get-room' + '?code=' + roomCode)
            .then((response) => response.json())
            .then((data) => {
                setVotesToSkip(data.votes_to_skip)
                setGuestCanPause(data.guest_can_pause)
                setIsHost(data.is_host)
            })

    return (
        <div>
            <h3>{roomCode}</h3>
            <p>Votes: {votesToSkip}</p>
            <p>Guest Can Pause: {String(guestCanPause)}</p>
            <p>Host: {String(isHost)}</p>
        </div>
    )
}

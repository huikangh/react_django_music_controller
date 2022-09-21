import React, { Component } from "react"
import { render } from "react-dom"
import HomePage from "./HomePage"


// this is a class component as opposed to a functional component
export default class App extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div className="center"> 
                <HomePage />
            </div>
        )
    }
}


const appDiv = document.getElementById("app")
render(<App />, appDiv)
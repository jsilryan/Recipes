import React from "react"
import Navbar from "./Navbar"
import {
    BrowserRouter as Router, //Helps app use react router
    Routes, //Create links and attach them to components
    Route //Attach routes to the components
} from "react-router-dom"
import HomePage from "./home"
import SignUp from "./signUp"
import Login from "./Login"
import CreateRecipe from "./CreateRecipe"

export default function App(){
    return (
        <React.StrictMode>
            <Router>
                <div className = "App">
                    <Navbar />
                    <Routes>
                        <Route path="/create_recipe" element ={<CreateRecipe />} />
                        <Route path="/login" element = {<Login />} />
                        <Route path="/signup" element = {<SignUp />} />
                        <Route path="/" element={<HomePage />} />
                    </Routes>
                </div>
            </Router>
        </React.StrictMode>
    )

}
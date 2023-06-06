import React from "react"
import {Link} from 'react-router-dom'

export default function Navbar() {
  return (
    <div className="navbar">
        <Link className="title-link" to="/">Recipes</Link>
        <Link className="links" to="/">Home</Link>
        <Link className="links" to="/signup">Sign Up</Link>
        <Link className="links" to="/login">Login</Link>
        <Link className="links" to="/create_recipe">Create Recipes</Link>
        <Link className="links">Log Out</Link>
        <div className="searches">
          <input type = "search" name="search" placeholder="Search here" className="search-bar"/>
          <button>
            <img className="search" src={require("./search1.png")} />
          </button>
          
        </div>
    </div>
  )
}


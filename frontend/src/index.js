import React from "react"
import ReactDOM from "react-dom"
import './index.css';
import App from './components/App'


function App3() {

    const [message, setMessage] = React.useState("Hello React")
    
    React.useEffect (
        ()=>{
            fetch("/recipe/hello")
            .then(response => response.json())
            // .then(data=> console.log(data))
            // setMessage(data.message)
            .then(data=> setMessage(data.message))
            .catch(error=>console.log(error))
        }, []
    )

    return(
        <div className = "App">
            {message}
        </div>
    )
}


// ReactDOM.render(<App />, document.getElementById("root"))
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <App />
)
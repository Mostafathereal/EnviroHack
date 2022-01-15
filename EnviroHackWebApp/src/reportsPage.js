import './App.css';
import React, { useRef } from 'react';
import ReactDOM from 'react-dom';

// GoogleMap - The Map itself
// withScriptjs & withGoogleMap - Embeds Google script on the page to load map correctly using higher order components
// Marker - Needed to add markers to the map
// InfoWindow - Shows a text window above a marker

class Reports extends React.Component{
  constructor(props){
    super(props);
    this.state = {
      email: this.props.email,
      password: "",
    }
  }

  render(){
    return (
      <div>
        <button onClick={() => console.log(this.state.email)}>Create Report</button>
      </div>
    );

  }

}

export default Reports;

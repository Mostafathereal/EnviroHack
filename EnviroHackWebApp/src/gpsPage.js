import './App.css';
import React, { useRef } from 'react';
import ReactDOM from 'react-dom';
import {GoogleMap, withScriptjs, withGoogleMap, Marker, InfoWindow} from 'react-google-maps';
import { withRouter } from './withRouter'
// GoogleMap - The Map itself
// withScriptjs & withGoogleMap - Embeds Google script on the page to load map correctly using higher order components
// Marker - Needed to add markers to the map
// InfoWindow - Shows a text window above a marker

var keyIn = false; // Temporary Fix
var mapsKey = ''; // Temporary Fix

// // Temporary Solution
// if (keyIn == false) {
//   mapsKey = prompt("What's the input API key?");
//   console.log(mapsKey);
//   keyIn = true;
// }
// Hard Coded (REMOVE FOR SURE)
mapsKey = 'AIzaSyAUTWxZ7iFZMXHdMBE_pmKJIgbqDEQw3f4';

class GpsInput extends React.Component{

  constructor(props){
    super(props);
    this.state = {
      address: "",
      mapPosition: {
        lat: 0,
        lng: 0,
      },
      markerPosition: {
        lat: 0,
        lng: 0,
      }
    }

    this.handleReportButton = this.handleReportButton.bind(this);
  }

  // When dragging marker over part of the map, change its lat and long
  onMarkerDragEnd = (event) => {
    let newLat = event.latLng.lat();
    let newLong = event.latLng.lng();

    this.setState({
      address: "",
      markerPosition: {
          lat: newLat,
          lng: newLong
      },
      mapPosition: {
          lat: newLat,
          lng: newLong
      },
  })

  }

  async handleReportButton(){
    console.log("Creating Report");
    // updating state of index
    // this.props.updateEmail("admin");
    console.log("1")
    const url = "/testpyconnect?lat=" + this.state.markerPosition.lat + '&lng=' + this.state.markerPosition.lng;
    console.log("2")
    const res = await fetch(url);
    console.log("3")

    // get imageData: json = JSON.parse(res); json.imageData

    // this.props.navigate('/reports');
    // console.log("4")
  }


/// take in gps coordinates
/// make call to send coordinates to python module through/handled by the backend
/// do it on another page

/// on gps page, have input field for gps coordinates and map to also use the as potential input
/// the maps take in regular street addresses and can let users see the map and click on it etc.

  render(){

    // Loads a map wrapped with higher order components at a given lat and long
    const WrappedMap = withScriptjs(withGoogleMap(prosp =>
      <GoogleMap
        defaultZoom={10}
        defaultCenter={{lat: this.state.mapPosition.lat, lng: this.state.mapPosition.lng}}
      >
        <Marker
          draggable={true}
          onDragEnd={this.onMarkerDragEnd}
          position={{ lat: this.state.markerPosition.lat, lng: this.state.markerPosition.lng }}
        >
          {<InfoWindow>
            <div>
              <span style={{ padding: 0, margin: 0, color: 'black' }}>Latitude: {this.state.markerPosition.lat}, <br />Longitude: {this.state.markerPosition.lng}</span>
            </div>
          </InfoWindow> }
        </Marker>
      </GoogleMap>
    ));

    return (
      <div>
        <div style={{ width: '60vw', height: '70vh' }}>

          {/* Displays the map  */}
          <WrappedMap googleMapURL={'https://maps.googleapis.com/maps/api/js?key='+mapsKey+'&v=3.exp&libraries=geometry,drawing,places'}
          loadingElement={<div style={{ height: "800%" }} />}
          containerElement={<div style={{ height: "250px" }} />}
          mapElement={<div style={{ height: "200%" }} />}
          />

        </div>
        <div>
          <div style={{float:"left"}}>
            <h3> Latitude:
              <input type="number"
              name="points"
              step="1"
              max="90"
              min="-90"
              value = {this.state.markerPosition.lat}
              onChange={(e) =>
                {
                  console.log(e.target.value)
                this.setState({markerPosition: {lat: parseFloat(e.target.value), lng: this.state.markerPosition.lng}, mapPosition: {lat: parseFloat(e.target.value), lng: this.state.markerPosition.lng}})}}
              />
            </h3>
          </div>

          <div style={{float: "left", marginLeft:"20px"}}>
            <h3> Longitude:
              <input type="number"
              name="points"
              step="1"
              max="180"
              min="-180"
              value = {this.state.markerPosition.lng}
              onChange={(e) =>
                {
                  console.log(e.target.value)
                this.setState({markerPosition: {lat: this.state.markerPosition.lat, lng: parseFloat(e.target.value)}, mapPosition: {lat: this.state.markerPosition.lat, lng: parseFloat(e.target.value)}})}}
              />
            </h3>
            <button onClick={this.handleReportButton}>Create Report</button>
          </div>
        </div>
      </div>
    );

  }

}

export default withRouter(GpsInput);

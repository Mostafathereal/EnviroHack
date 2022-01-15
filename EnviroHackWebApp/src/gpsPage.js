import './App.css';
import React, { useRef } from 'react';
import ReactDOM from 'react-dom';
import {GoogleMap, withScriptjs, withGoogleMap, Marker, InfoWindow} from 'react-google-maps';
import { withRouter } from './withRouter';
// GoogleMap - The Map itself
// withScriptjs & withGoogleMap - Embeds Google script on the page to load map correctly using higher order components
// Marker - Needed to add markers to the map
// InfoWindow - Shows a text window above a marker


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
    this.props.updateEmail("admin");
    // const url = "/testpyconnect?lat=" + this.state.markerPosition.lat + '&lng=' + this.state.markerPosition.lng;
    // const res = await fetch(url);

    this.props.navigate('/reports', {state : {email : "admin"}});

    // get imageData: json = JSON.parse(res); json.imageData
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
      <div style={{ width: '80vw', height: '100vh' }}>

        {/* Displays the map  */}
        <WrappedMap googleMapURL={'https://maps.googleapis.com/maps/api/js?key=AIzaSyAUTWxZ7iFZMXHdMBE_pmKJIgbqDEQw3f4&v=3.exp&libraries=geometry,drawing,places'}
        loadingElement={<div style={{ height: "100%" }} />}
        containerElement={<div style={{ height: "400px" }} />}
        mapElement={<div style={{ height: "100%" }} />}
        />

        <h3>Latitude: {this.state.markerPosition.lat}</h3> <br />
        <h3>Longitude: {this.state.markerPosition.lng}</h3>

        <button onClick={this.handleReportButton}>Create Report</button>
      </div>
    );
  }
}

export default withRouter(GpsInput);

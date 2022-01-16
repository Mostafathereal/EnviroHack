import React from 'react';
import ReactDOM, { render } from 'react-dom';
import './index.css';
import GpsInput  from './gpsPage';
import Reports from './reportsPage';
import Indices from './indicesPage';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom'

// ReactDOM.render(
//   <React.StrictMode>
//     <Reports />
//   </React.StrictMode>,
//   document.getElementById('root')
// );

class Index extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      email: "",
      NDWIImageData: "",
      NDVIImageData: "",
      BAIImageData: "",
      segImageData: ""
    }
    this.updateState = this.updateState.bind(this)
  }

// used to allow other components to update state for the props that would be passed to other components
// need to change name to make general
  updateState(e) {
    console.log("hello")
    this.setState(e)
  }

            // <Route exact path="/reports" element={<Reports />}/>

  render() {
    return (
      <div>
        <Router>
          <Routes>
            <Route exact path="/gps" element={<GpsInput updateState={this.updateState}/>}/>
            <Route exact path="/" element={<Navigate to="/gps" />}/>
            <Route exact path="/reports" element={<Reports NDWIImageData={this.state.NDWIImageData} NDVIImageData={this.state.NDVIImageData} BAIImageData={this.state.BAIImageData} segImageData={this.state.segImageData}/>}/>
            <Route exact path="/indices" element={<Indices NDWIImageData={this.state.NDWIImageData} NDVIImageData={this.state.NDVIImageData} BAIImageData={this.state.BAIImageData} segImageData={this.state.segImageData}/>}/>
          </Routes>
        </Router>
      </div>
    );
  }
}

render(<Index />, document.getElementById("root"));

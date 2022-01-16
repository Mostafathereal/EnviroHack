import React, from 'react';
import { withRouter } from './withRouter'

class Indices extends React.Component {
  constructor(props){
    super(props);
  }

render() {
  const { NDWIImageData, NDVIImageData, BAIImageData, segImageData } = this.props;

  return(
    <img src={"data:image/jpg;base64," + (NDWIImageData ? NDWIImageData : "iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==")} alt="Red dot" />
    <img src={"data:image/jpg;base64," + (NDVIImageData ? NDVIImageData : "iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==")} alt="Red dot" />
    <img src={"data:image/jpg;base64," + (BAIImageData ? BAIImageData : "iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==")} alt="Red dot" />
    <img src={"data:image/jpg;base64," + (segImageData ? segImageData : "iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==")} alt="Red dot" />
  )}
}

export default withRouter(Indices);

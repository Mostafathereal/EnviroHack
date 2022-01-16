import React, { useRef } from 'react';
import TableCell from "@material-ui/core/TableCell";
import TableRow from "@material-ui/core/TableRow";
import Box from "@material-ui/core/Box";

class Cell extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      isView: false,
    }
  }


  handleView(){
    //console.log(e)
    NDWIImageData = this.props.NDWIImageData;
    this.setState({isView: true})
    /// to do print out the image data
  }

render() {
  const { date, reportName, NDWIImageData } = this.props;
  var isView = this.state.isView;

  return(
  <TableRow>
    <TableCell
      classes="cellRoot"
      component="th"
      variant="head"
      scope="row"
    >
      {date}
    </TableCell>
    <TableCell>
      {reportName}
    </TableCell>
    <TableCell>
      <button onClick={this.handleView}>View</button>
    </TableCell>
    <TableCell>
      <button>Export</button>
    </TableCell>
  </TableRow>
  <div>
    {isView
      ? <image></image>
      : <h></h>
    }
  </div>
  )}
}

export default Cell;

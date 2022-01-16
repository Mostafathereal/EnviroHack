import React, { useRef } from 'react';
import TableCell from "@material-ui/core/TableCell";
import TableRow from "@material-ui/core/TableRow";
import Box from "@material-ui/core/Box";
import { withRouter } from './withRouter'

class Cell extends React.Component {
  constructor(props){
    super(props);
  }


  handleView(){
    this.props.navigate('/indices');
    //console.log(e)
    /// to do print out the image data
  }

render() {
  const { date, reportName } = this.props;

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
  )}
}

export default withRouter(Cell);

import React, { useRef } from 'react';
import TableCell from "@material-ui/core/TableCell";
import TableRow from "@material-ui/core/TableRow";
import Box from "@material-ui/core/Box";

class Cell extends React.Component {
  constructor(props){
    super(props);
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
      <button>View</button>
    </TableCell>
    <TableCell>
      <button>Export</button>
    </TableCell>
  </TableRow>
  )}
}

export default Cell;

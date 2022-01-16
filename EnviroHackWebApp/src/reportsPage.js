import './App.css';
import React, { useRef } from 'react';
import ReactDOM from 'react-dom';
import Grid from "@material-ui/core/Grid";
import Card from "@material-ui/core/Card";
import Box from "@material-ui/core/Box";
import Typography from "@material-ui/core/Typography";
import CardHeader from "@material-ui/core/CardHeader";
import TableContainer from "@material-ui/core/TableContainer";
import Table from "@material-ui/core/Table";
import TableCell from "@material-ui/core/TableCell";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import TableBody from "@material-ui/core/TableBody";
import Cell from "./cells"

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
    var result = "";
    var name = "";
    for(var i=0; i < 3; i++){
      name = "reportName"
      result='<Cell date="01/16/22" reportName=' + name + '/>';
    }


    return (
      <div>
        <Card style = {{width:"150vh"}}>
          <CardHeader
            subheader={
              <Grid
                container
                component={Box}
                alignItems="center"
                justifyContent="space-between"
              >
                <Grid item xs="auto">
                  <Box
                    component={Typography}
                    variant="h3"
                    marginBottom="0!important"
                  >
                    Reports
                  </Box>
                </Grid>
                <Grid item xs="auto">
                  <Box
                    justifyContent="flex-end"
                    display="flex"
                    flexWrap="wrap"
                  >
                    <button
                      variant="contained"
                      color="primary"
                      size="small"
                    >
                      See all
                    </button>
                  </Box>
                </Grid>
              </Grid>
            }
          ></CardHeader>
          <TableContainer>
            <Box
              component={Table}
              alignItems="center"
              marginBottom="0!important"
            >
              <TableHead>
                <TableRow>
                  <TableCell>
                     Date
                  </TableCell>
                  <TableCell>
                    Report Name
                  </TableCell>
                  <TableCell>
                  </TableCell>
                  <TableCell>
                  </TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                <Cell date="01/16/22" reportName="reportName"/>
              </TableBody>
            </Box>
          </TableContainer>
        </Card>
      </div>
    );
  }
}

export default Reports;

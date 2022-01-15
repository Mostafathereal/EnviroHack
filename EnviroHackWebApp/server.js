//create express app
const express = require('express');
const app = express();
const mysql = require('mysql');
const { io } = require('socket.io-client');

app.get('/', function (req, res) {
   res.send('Hello World! test');


});

app.get('/test', function (req, res) {
    var con = mysql.createConnection({
        host: "35.243.200.4",
        user: "dev",
        password: "password123",
        database: 'enviroheal'
      });

      con.connect(function(err) {
        if (err) throw err;
        con.query("SELECT * FROM accounts", function (err, result, fields) {
          if (err) throw err;
          console.log(result);
          res.json({message: result});
        });
      });

});

app.get('/login/:email', function (req, res) {
  var email = req.params.email;
  var con = mysql.createConnection({
      host: "35.243.200.4",
      user: "dev",
      password: "password123",
      database: 'enviroheal'
    });

    con.connect(function(err) {
      if (err) throw err;
      con.query("SELECT * FROM accounts WHERE email='" + email + "'", function (err, result, fields) {
        if (err) throw err;
        console.log(result);
        res.json({message: result});
      });
    });
});

app.get('/testpyconnect', function(req, res){
  console.log("entered in testpyconnect");

  const socket = io("http://localhost:3050");
  var lat = req.query.lat;
  var lng = req.query.lng;

  socket.on("connect", () => {
    // either with send()
    socket.send("Hello!");
    // // or with emit() and custom event names
    socket.emit("my_message", lat + " " + lng);
    console.log('connected ... ');
  });


  // handle the event sent with socket.send()
  socket.on("my_message", data => {
    console.log(data);
  });

  // handle the event sent with socket.emit()
  socket.on("my_message_response", data => {
    console.log(data);
    res.json(data);
  });

  //close socket connection
  // socket.disconnect();
})


//make event handlers to send gps coordinates
//make event handler to receive image from python module, decode and send to frontend

var server = app.listen(5000, function () {
    console.log('Server is listening on port 5000...');
});


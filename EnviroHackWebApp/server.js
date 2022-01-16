//create express app
const express = require('express');
const app = express();
const mysql = require('mysql');
const { io } = require('socket.io-client');
//Call body-parser for POST data handling
var bodyParser = require("body-parser");
app.use(bodyParser.urlencoded({ extended: false }));

const port = 3000;
const host = 'localhost'

const Sequelize = require("sequelize-cockroachdb");

// For secure connection to CockroachDB
const fs = require('fs');

// Connect to CockroachDB through Sequelize
var sequelize = new Sequelize({
  dialect: "postgres",
  username: "chris",
  password: "thisismysql123",
  host: host,
  port: port,
  database: "reports",
  dialectOptions: {
    ssl: {

      //For secure connection:
      ca: fs.readFileSync('./certs/root.crt')
              .toString()
    },
  },
  logging: false,
});

//Define the table we'll be working with in CockroachDB

const report = sequelize.define("report", {
    id: {
      type: Sequelize.INTEGER,
      autoIncrement: true,
      primaryKey: true
    },
    waterInd: {
        type: Sequelize.TEXT
    },
    vegeInd: {
      type: Sequelize.TEXT
    },
    burnInd: {
      type: Sequelize.TEXT
    },
    segData: {
      type: Sequelize.TEXT
    },
});

//Create a page that lists our contacts already in the database

app.get('/list', (req, res) => {

    //Get our data from CockroachDB
    report.sync({
         force:false,
    })
    .then(function() {
       return report.findAll();
    })

    // .then(function (report) {
    //     //Render output from CockroachDB using our PUG template
    //     res.render('list', { report : report });
    // })

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

    json = res.json()
    var waterIndRes = JSON.parse(json).NDWIImageData

    //Add our POST data to CockroachDB via Sequelize
    report.sync({
        force: false,
    })
        .then(function () {
        // Insert new data into People table
        return report.bulkCreate([
            {
            waterInd: waterIndRes,
            },
        ]);
        })

    	  //Error handling for database errors
        .catch(function (err) {
        console.error("error: " + err.message);
        });

        //Tell them it was a success
        res.send('Submitted Successfully!<br /> WaterInd:  ' + waterInd);
  });

  //close socket connection
  // socket.disconnect();
})


//make event handlers to send gps coordinates
//make event handler to receive image from python module, decode and send to frontend

// var server = app.listen(5000, function () {
//     console.log('Server is listening on port 5000...');
// });

app.listen(port, host, () => {
    console.log(`Server started at ${host} port ${port}`);
});

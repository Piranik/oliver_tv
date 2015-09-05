var express = require('express');
var app = express();

var http = require('http').Server(app);
var io = require('socket.io')(http);
var fs = require('fs');
var path = require('path');

var spawn = require('child_process').spawn;
var proc;

app.use('/', express.static(path.join(__dirname, 'stream')));

app.get('/', function(req, res) {
	  res.sendFile(__dirname + '/index.html');
});


var sockets = {};

io.on('connection', function(socket) {

  sockets[socket.id] = socket;
  console.log("Total clients connected : ", Object.keys(sockets).length);

  socket.on('disconnect', function() {
    delete sockets[socket.id];

    // no more sockets, kill the stream
    if (Object.keys(sockets).length == 0) {
      app.set('watchingFile', false);
      if (proc) proc.kill();
      fs.unwatchFile('./stream/image_stream.jpg');
    }
  });

  socket.on('start-stream', function() {
    startStreaming(io);
  });

});

http.listen(3000, function() {
  console.log('listening on *:3000');
});

function stopStreaming() {
  if (Object.keys(sockets).length == 0) {
    app.set('watchingFile', false);
    if (proc) proc.kill();
    fs.unwatchFile('./stream/image_stream.jpg');
  }
}

function startStreaming(io) {

  if (app.get('watchingFile')) {
    io.sockets.emit('liveStream', 'image_stream.jpg?_t=' + (Math.random() * 100000));
    return;
  }

  var args = ["-w", "480", "-h", "480", "-o", "./stream/image_stream.jpg", "-t", "999999999", "-tl", "100","-rot","180"];
  //proc = spawn('raspistill', args);

  console.log('Watching for changes...');

  app.set('watchingFile', true);

  //fs.watchFile('./stream/image_stream.jpg', 
  setInterval(function(current, previous) {
	console.log('emitting..');
	var cp = require("child_process");
	cp.exec("compare -metric mae ./background/notpresent2.jpg ./stream/image_stream.jpg ./stream/difference.png", function (err, stdout, stderr) {
		console.log(stderr);	

		var regExp = /\(([^)]+)\)/;
  		var matches = regExp.exec(stderr);
		if (matches[1]>0.05) {
			console.log('Oliver is present!');
		}
	});
	
	io.sockets.emit('liveStream', 'image_stream.jpg?_t=' + (Math.random() * 100000));
  },1000);

}

process.stdin.resume();//so the program will not close instantly

function exitHandler(options, err) {
    if (options.cleanup) spawn('pkill raspistill');
    if (err) console.log(err.stack);
    if (options.exit) process.exit();
}

//do something when app is closing
process.on('exit', exitHandler.bind(null,{cleanup:true}));

//catches ctrl+c event
process.on('SIGINT', exitHandler.bind(null, {exit:true}));

//catches uncaught exceptions
process.on('uncaughtException', exitHandler.bind(null, {exit:true}));


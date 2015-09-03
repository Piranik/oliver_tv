# Oliver TV

A NodeJS application that allows you to stream your cat onto a webserver using a Raspberry Pi. It is somewhat based off the [RPi-KittyCam](https://github.com/schollz/RPi-KittyCam) and [This IoT article on streaming from Rpis](http://thejackalofjavascript.com/rpi-live-streaming).

# Install

Install Node using

> sudo apt-get install nodejs npm

and since something is wrong with the node being declared you might have to use

> sudo apt-get install nodejs-legacy

Then install ``forever`` and ``gyp`` globally:

> sudo npm install -g node-gyp forever

Then you can clone the repositor and simply run

> npm install

# Run

Use forever to run like this:

> forever start index.js

And goto your web browser to see the TV!

# To-do

- Add button to play can opening-sound to aquire cat
- Add button to deliver treat
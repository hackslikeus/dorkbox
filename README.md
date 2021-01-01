# dorkbox
yet another internet radio mpd client.  It only consists of one python file and one html file on purpose.

MPD client solely focused on internet radio stations.  For now, stations are stored inside the Python file, called into the html page using sql lite. Most folks will want to edit  to their liking which are very easy to locate inside the python file, with no further instructions needed.  Need to bring to Tiny DB and keep json file outside python (todo).

Tornado webserver will listen on port 8080 unless you set web = false, then port 5000 will be used for dev.

Bootstrap4 and Jumbotron will offer areas of customization and gussey-it-up potential.  I experimented with a few background images for jumbotron with mixed results, YMMV.  -  Speaking of images, I purposely left out the radio station url images because, quite frankly, I put more time and effort in attempts at fetching and displaying these than the original "artist" put into creating them, so if you want eye candy, check out mtv.

Instructions for pi users:  Download python file and bootstrap.html file found in templates folder.  create a folder on the server pi and deploy, keeping the structure in tact.  note there is a reference or two in the python file to the html page, so rename at your risk, but not a big deal. 

Prerequisites include Pip3, python3, Flask, Sql-lite, and tornado.  Almost forgot, MPD and MPC -  Once you have all the programs loaded and the files in place, simply run the python program and navigate to the serving Pi's ip address at port 8080( for example "10.0.0.112:8080").  You will see the results of the stations loading in your command line.  Ctrl-C will stop the python program.

Check alsa volume levels before first run as many pi's will have volume at 100% by default.  MPC commands from command line or web page will also alter volume.  I recommend  volume at 25% to start.

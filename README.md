# dorkbox
![Screenshot_2021-01a](https://user-images.githubusercontent.com/16979775/104129177-399c9c80-5331-11eb-8f90-57e8cf368a43.png)
another internet radio mpd client.  A simple Flask project consisting of one python file, one html file and a csv template for stations and their urls.

this low resource MPD client is solely focused on internet radio.  Stations are listed in a csv file, imported by python program and displayed as a playlist on an intuitive web page using Flask. With simplicity in mind, the goal of this project is to go from startup to music in as few clicks as possible. Most folks will want to edit the list of stations in the csv file to their liking - with no further instructions needed.  Since the code is mainly python, any pi or SBC should be able to run this application.  Ideally, the python program could be run at boot, and as a background service using systemd, rc.local etc.

Tornado webserver will listen on port 8080 unless you set web = false, then port 5000 will be used for dev.

Latest changes reflect different architecture to make the station list more scalable.  Bootstrap is still being utilized as the rendering web platform, however jumbotron and logo images are no longer in favor, and have been replaced with table frame and minimal search capabilities to sort through station lise. 

Instructions for pi users:  Download python file, index.html, and moodies.csv files.  Create a folder on the server pi, ie. "dorkbox",  with a subdirectory for templates, (a flask thing) where the index.html bootstrap file should reside. The csv file will reside in the same folder as the python file.  Note there is a reference or two in the python file for file name locations, so rename at your risk, but not a big deal.

Must have Prerequisites include MPD, MPC, Pip3, python3, Flask, and Tornado.  You should already have mpd configured and soundcard configuration already complete to make trouble shooting easier later on.  Once you have all the programs loaded and the files in place, simply run the python program from the command line. A one line indicator on the command line will alert you when it is OK to navigate to the web page.
Navigate to the serving Pi's ip address at port 8080( for example "10.0.0.112:8080") using a web browser.  Hit a play button and that should be it. 
Check your mpd.conf or soundcard settings if no audio eminates from your speakers.

Ctrl-C will stop the python program.  I recommend running a systemd service to have the python program run at startup.

Finally, the latest revisions were included to make dorkbox a standalone application, or to be included as an ADDON to RPI Monitor project and run from RPI-Monitor.

***Check alsa volume levels before first run as many pi's will have volume at 100% by default.  MPC commands from command line or web page will also alter volume.  I recommend  volume at 25% to start.
[instructions.txt](https://github.com/hackslikeus/dorkbox/files/7669629/instructions.txt)

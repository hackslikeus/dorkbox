# dorkbox
![Screenshot_2021-01a](https://user-images.githubusercontent.com/16979775/104129177-399c9c80-5331-11eb-8f90-57e8cf368a43.png)
yet another internet radio mpd client.  A simple Flask project consisting of one python file, one html file and a csv template for stations and their urls.

With a raspberry pi zero w as the target server, this low power MPD client is solely focused on internet radio.  Stations are listed in a csv file, imported by python program and displayed as a playlist on an intuitive web page using Flask. With simplicity in mind, the goal of this project is to go from startup to music in as few clicks as possible. Most folks will want to edit the list of stations to their liking - with no further instructions needed.  Since the code is mainly python, any pi or SBC should be able to run this application.  Ideally, the python program could be run at boot, and as a background service using systemd, rc.local etc.

Tornado webserver will listen on port 8080 unless you set web = false, then port 5000 will be used for dev.

Bootstrap4 and Jumbotron will offer areas for customization and gussey-it-up potential.  I experimented with a few background images for the jumbotron with mixed results; YMMV.  -  Speaking of images, The purple box pattern in the screenshot is actually a geopattern svg of the word "Dorkbox Radio". 

Instructions for pi users:  Download python file, bootstrap.html, and stations.csv files.  Create a folder on the server pi, ie. "dorkbox",  with a subdirectory for templates, (a flask thing) where the index.html bootstrap file should reside. The csv file will reside in the same folder as the python file.  Note there is a reference or two in the python file to the html page, so rename at your risk, but not a big deal.

Tested on Armban, Dietpi and Raspbian os. Prerequisites include MPD, MPC, Pip3, python3, Flask, and Tornado.  Once you have all the programs loaded and the files in place, simply run the python program from the command line. A one line indicator on the command line will alert you when it is OK to navigate to the web page.
Navigate to the serving Pi's ip address at port 8080( for example "10.0.0.112:8080") using a web browser.  Hit a play button, You will see the station logo on the web page, and with luck, music will fill your ears.  

Ctrl-C will stop the python program.  Make sure /etc/mpd.conf is properly configured. 

***Check alsa volume levels before first run as many pi's will have volume at 100% by default.  MPC commands from command line or web page will also alter volume.  I recommend  volume at 25% to start.

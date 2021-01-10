# dorkbox
![Screenshot_2021-01a](https://user-images.githubusercontent.com/16979775/104129177-399c9c80-5331-11eb-8f90-57e8cf368a43.png)
yet another internet radio mpd client.  It only consists of one python file and one html file, and a csv file on purpose.

MPD client solely focused on internet radio stations.  Stations are listed in a csv file, imported by python progrm without pandas. Most folks will want to edit this list to their liking- with no further instructions needed.  

Tornado webserver will listen on port 8080 unless you set web = false, then port 5000 will be used for dev.

Bootstrap4 and Jumbotron will offer areas of customization and gussey-it-up potential.  I experimented with a few background images for jumbotron with mixed results, YMMV.  -  Speaking of images, I purposely left out the radio station url images because, quite frankly, I put more time and effort in attempts at fetching and displaying these than the original "artist" put into creating them, so if you want eye candy, check out mtv.

Instructions for pi users:  Download python file and bootstrap.html file found in templates folder.  create a folder on the server pi and deploy, keeping the structure in tact.  note there is a reference or two in the python file to the html page, so rename at your risk, but not a big deal. Stations.csv file should reside in same folder as python program, if moved the reference will need to be noted in the location of the filename.  A sample .csv file is found in the templates, and easilly editable without changing the python code. (version #1 compared to #0)

Prerequisites include Pip3, python3, Flask, and tornado.  Almost forgot, MPD and MPC -  Once you have all the programs loaded and the files in place, simply run the python program and navigate to the serving Pi's ip address at port 8080( for example "10.0.0.112:8080").  You will see the results of the stations loading in your command line.  Ctrl-C will stop the python program.

Check alsa volume levels before first run as many pi's will have volume at 100% by default.  MPC commands from command line or web page will also alter volume.  I recommend  volume at 25% to start.

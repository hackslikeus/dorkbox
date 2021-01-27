# Ingredients: Flask, Tornado and some system functions
from flask import Flask, g, render_template, redirect, request
import csv
import sys, os
import time
from time import sleep
from subprocess import *
# Tornado web server
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop


# Tell Flask and Tornado production site, not safe to use dev env
web = True

#keep below:
#location of the csv file in same folder otherwise direct
filename = "/home/pi/dorkbox/stations.csv"

# Initialize Flask.
if web:
    app = Flask(__name__)


    @app.route('/')
    def sl():
      with open(filename, mode = 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        data = csv.reader(csvfile, delimiter=',')
        first_line = True
        entries = []
        for row in data:
          if not first_line:
            entries.append({
               "id": row[0],
               "name": row[1],
               "url": row[2],
               "descr": row[3],
               "logo": row[4]
               })

          else:
            first_line = False
      return render_template('index.html', entries=entries)

# To execute commands outside of Python
    def run_cmd(cmd):
        p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
        output = p.communicate()[0]
        return output


    #Adjust Volume Down - is now working with Alsa
    @app.route('/volumed')
    def volumed():
        run_cmd('mpc volume -10')
        return redirect ('/')


    #stop the music...
    @app.route('/stop')
    def stop_music():
        run_cmd('mpc stop')
        return redirect('/')


 # Play a stream from the id provided in the html string. the row is a string, converted to a list
    # use mpc as actual program to handle the mp3 streams.
    @app.route('/<int:stream_id>')
    def mpc_play(stream_id):
        with open(filename, mode = 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            data = list(csvfile)
        for row in data:
            url_here = (data[stream_id])
            splitz = (url_here).split(",")
            url = (splitz[2])
            run_cmd('mpc clear')
            run_cmd( ['mpc add %s' % (url)])
            print (url)
            run_cmd('mpc play')
            sleep(1)
            general_Data = {
            'title' : 'Un-A-Ware v1'}
            station = (splitz[1])
            logo = (splitz[4])
            #artist =os.popen('mpc -f %artist%').readline()
            song = os.popen('mpc -f %title%').readline()
            return render_template('index.html', station=station, logo=logo, song=song, **general_Data)
    print("proceed to your servers ip address at port 8080 using a web browser") #alert user program is running

#Not sure if the below is needed, was working on LCD screen, will leave as it is harmless
    def loop():
        while True:
            song = os.popen('mpc -f %title%').readline()
            sleep(10)
            return render_template('index.html', song=song)


# Shutdown the computer now on navbar
    @app.route('/shutdown')
    def shutdown_now():
        run_cmd('sudo shutdown -h now ')
        return 'Adios!'


# To gracefully reboot - used for modal
    @app.route('/reboot', methods=['POST', 'GET'])
    def reboot():
        IOLoop.instance().stop()
        run_cmd('sudo reboot now')
        return 'rebooting the server.  Use your browsers back button to retun. \nSee you soon :)'

# To gracefully shutdown the web application -not needed
    @app.route('/shutdown_server', methods=['POST', 'GET'])
    def shutdown():
        IOLoop.instance().stop()
        return 'Shutting down the server.\nSee you soon :)'

#Adjust Volume up is working with Alsa
    @app.route('/volumeu')
    def volumeu():
        run_cmd('mpc volume +10')
        return redirect ('/')
    
    # Is MPD playing a song?
#    def mpc_status():
#        playing = (os.popen('mpc status | grep playing')).readline()
#        if playing=="":
#            return(0)
#        elif playing != "":
#            return(1)
        
    def current_song():
        song = os.popen('mpc -f %title%').readline()
        return(song.strip())

    def current_artist():
        title = os.popen('mpc -f %artist%').readline()
        return(title.strip())

    def current_album():
        album = os.popen('mpc -f %album%').readline()
        return(album.strip())

    @app.route('/', methods=['GET', 'POST'])
    def radio_song():
        sstring = os.popen('mpc -f %title%').readline()
        astring = os.popen('mpc -f %title%').readline()
        song = sstring.split('-')[1]
        artist = astring.split('-')[0]
        return render_template('index.html', artist=artist, song=song)


if __name__ == "__main__":
    #create_whole_db(DATABASE)
    #app.run()
    if web:
        http_server = HTTPServer(WSGIContainer(app))
        http_server.listen(8080)
        IOLoop.instance().start()


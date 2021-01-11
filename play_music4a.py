# Ingredients: Flask, SQLite and some system functions
from flask import Flask, g, render_template, redirect, request
import csv 
import sys, os
from subprocess import *
# Tornado web server
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop


# Tell Flask and Tornado production site, not safe to use dev env
web = True

#keep below:
#location of the csv file in same folder otherwise direct
filename = "stations5.csv"

# Initialize Flask.
if web:
    app = Flask(__name__)
    
#class streams():    
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
               "descr": row[3]
               })
            
          else:
            first_line = False
      return render_template('index.html', entries=entries)

# To execute commands outside of Python
    def run_cmd(cmd):
        p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
        output = p.communicate()[0]
        return output

    
#if web:
    @app.route('/')
    def show_entries():
        general_Data = {
        'title' : 'YourNameHereware v1.0'}
 #       stream_entries = return_dict(DATABASE) -deprecated
        return render_template('index.html', **general_Data)
    

    #Adjust Volume Down - is now working
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
            return redirect('/')
        
# Shutdown the computer now on navbar
    @app.route('/shutdown', methods=['POST', 'GET']))
    def shutdown_now():
        run_cmd('sudo shutdown -h now')
        return 'Adios!'

# Reboot the computer now on navbar
    @app.route('/reboot', methods=['POST', 'GET']))
    def reboot():
        #IOLoop instance().stop()
        run_cmd('sudo reboot now')
        return 'Use browser back button after one minute. \n See you soon:)'

    
     #Adjust Volume up is working
    @app.route('/volumeu')
    def volumeu():
        run_cmd('mpc volume +10')
        return redirect ('/')

# Here comes the main call.
# Use Tornado from ths point
if __name__ == "__main__":
    #use below for non web test comment out for prod
    #app.run()
    if web:
        http_server = HTTPServer(WSGIContainer(app))
        http_server.listen(8080)
        IOLoop.instance().start()


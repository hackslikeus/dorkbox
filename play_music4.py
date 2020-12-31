# Some necessary includes: Flask, SQLite and some system functions
from flask import Flask, g, render_template, redirect, request
import sqlite3 as lite
#import tinydb
import sys, os
from subprocess import *
# Tornado web server
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop


# Database name. You may use any other database name you like.
DATABASE = '/home/pi/dorkbox/streams.db'

# Just a debugging flag to switch off Flask and Tornado
web = True

# Should be moved to json text file...
# for now - creates the SQLite database
# change/add the music streams permissable.
def create_whole_db(DATABASE):
    table_data = {
    'streams':(
    (1,'Lounge-Radio', r'http://nl1.streamhosting.ch/', 'Swiss Chill'),
    (2,'Zen fm',r'http://lb.zenfm.be/zenfm.mp3', 'Cool Grooves and Tasty tunes'),
    (3,'Soma - Groove Salad',r'http://ice1.somafm.com/groovesalad-256-mp3', 'A nicely chilled plate of ambient/downtempo beats and grooves'),
    (4,'The Jazz Groove', r'http://east-mp3-128.streamthejazzgroove.com/', 'Laid Back Jazz'),
    (5,'Soma - Beat Blender', r'http://ice6.somafm.com/beatblender-128-mp3', 'A late night blend of deep-house and downtempo chill'),
    (6,'Scratch Radio', r'http://www.scratchradio.ca:8000/', 'Canadas finest Reggae'),
    (7,'Soma - Illinois Street Lounge', r'http://ice4.somafm.com/illstreet-128-mp3', 'Classic bachelor pad, playful exotica and vintage music of tomorrow'),
    (8,'ChillTrax', r'http://server1.chilltrax.com:9000/', 'Ambient Chill'),
    (9,'Soma - Lush', r'http://ice6.somafm.com/lush-128-mp3', 'Sensuous and mellow vocals, mostly female, with an electronic influence'),
    (10,'Soma - Underground 80s', r'http://ice4.somafm.com/u80s-256-mp3', 'Early 80s UK Synthpop and a bit of New Wave'),
    )}
    #connect to database
    db_connection = lite.connect(DATABASE)
    cursor = db_connection.cursor()
    #create table
    cursor.execute("DROP TABLE IF EXISTS Streams")
    cursor.execute("CREATE TABLE Streams" +\
    "(id INT, name VARCHAR(255), link VARCHAR(255), descr VARCHAR(255))")
    for data in table_data['streams']:
        qstr = "INSERT INTO Streams " +\
               "(id, name, link, descr) values ('%d', '%s', '%s', '%s')" %(data[0], data[1], data[2], data[3])
        print (qstr)
        cursor.execute(qstr)
        #necessary - at least in windows...
        db_connection.commit()
    db_connection.close()

# This function reads out the table streams from the database.
#should be moved to json later on.
# It returns a list of dictionaries Flask and Jinja can process.
def return_dict(DATABASE):
    db_connection = lite.connect(DATABASE)
    with db_connection:
        cursor = db_connection.cursor()
        data = cursor.execute("SELECT id, name, link, descr FROM Streams")
        rows = data.fetchall()

        #create list of dictionaries
        dict_here = [dict(id=row[0], name=row[1], link=row[2], descr=row[3]) for row in rows]
        return dict_here

# To execute commands outside of Python
def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
    output = p.communicate()[0]
    return output

# Initialize Flask.
if web:
    app = Flask(__name__)

if web:
    @app.route('/')
    def show_entries():
        general_Data = {
        'title' : 'Garyware v0.22'}
        stream_entries = return_dict(DATABASE)
        return render_template('main4_bootstrap.html', entries = stream_entries, **general_Data)

    #Adjust Volume Down - is now working
    @app.route('/volumed')
    def volumed():
        run_cmd('mpc volume -10')
        return redirect ('/')


    # We do stop the music...
    @app.route('/stop')
    def stop_music():
        run_cmd('mpc stop')
        return redirect('/')

    # Play a stream from the id provided in the html string. 
    # We use mpc as actual program to handle the mp3 streams.
    @app.route('/<int:stream_id>')
    def mpc_play(stream_id):
        db_connection = lite.connect(DATABASE)
        with db_connection:
            cursor = db_connection.cursor()
            data = cursor.execute("SELECT link FROM Streams WHERE id='%d'" % (stream_id) )
            link_here = data.fetchone()[0]
            run_cmd('mpc clear')
            run_cmd( ['mpc add %s' % (link_here)])
            print (link_here)
            run_cmd('mpc play')
            return redirect('/')

    # Shutdown the computer -now on navbar - use "sudo halt" if you want music to resume on pi startup
    @app.route('/shutdown')
    def shutdown_now():
        run_cmd('sudo shutdown -h now')
        return 'Adios!'

    # To gracefully reboot - found on modal
    @app.route('/reboot', methods=['POST', 'GET'])
    def reboot():
        IOLoop.instance().stop()
        run_cmd('sudo reboot now')
        return 'rebooting the server.\nSee you soon :)'

     #Adjust Volume up is working
    @app.route('/volumeu')
    def volumeu():
        run_cmd('mpc volume +10')
        return redirect ('/')


# Here comes the main call.
# See how simple it is to launch a Tornado server with HTTPServer.
if __name__ == "__main__":
    create_whole_db(DATABASE)

    if web:
        http_server = HTTPServer(WSGIContainer(app))
        http_server.listen(8080)
        IOLoop.instance().start()


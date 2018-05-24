import os, os.path #
import random #
import sqlite3 #the libery for the code to create a SQLite3 system 
import string #
import time #the libery for the time rellated commands like the time.sleep command to set a time it will whaite untill the time is up.
import datetime


import cherrypy #


DB_STRING = "Logging.db"
colors = ["#000000","#FFFF00","#FF0000","#FF00FF","#00FF00","#0000FF","#FFD700","#A52A2A","#00FFFF","#EE82EE","#FF69B4","#AAAAAA"]
class TemperatureDatabase(object):#
    @cherrypy.expose
    def index(self):
        return open('index.html')#

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def todaysdata(self):
        #gets todays data from the database
        #todays data is time is grather than midnight
        midnight = datetime.datetime.combine(datetime.datetime.today(), datetime.time.min)
        midnightunix = time.mktime(midnight.timetuple())
        return self.datasince(midnightunix)
        
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def latestdata(self, since ):
        #gets todays data from the database
        #todays data is time is grather than midnight
        return self.datasince(since)
        
           
    
    def datasince(self, sinceunix):
        with sqlite3.connect(DB_STRING) as c:
            SQL = "SELECT * FROM Logging_Table WHERE TIME >="+str(sinceunix)
            print (SQL)
            r = c.execute(SQL)
            data = r.fetchall()

            Measurements = {"HUMIDTY":{
                        'type':"scatter",
                        'mode':"lines",
                        'name':"humidity",
                        'x':[],
                        'y':[],
                        'line':{"color": "blue"}
                        },
                            "TEMP":{
                        'type':"scatter",
                        'mode':"lines",
                        'name':"temperature",
                        'x':[],
                        'y':[],
                        'line':{"color": "red"}
                        }
                            }
            numcount = 0
            #loop threw the arrys to get out data for each mesuement
            for row in data:
                [TIME, HUMIDITY, CO2, TEMP] = row
                #checks if the room exsists and creates one if it does not exsist
                timeonly = datetime.datetime.fromtimestamp(TIME).strftime('%H:%M:%S')
                Measurements["HUMIDTY"]['x'].append(timeonly)
                Measurements["HUMIDTY"]['y'].append(HUMIDITY)

                Measurements["TEMP"]['x'].append(timeonly)
                Measurements["TEMP"]['y'].append(TEMP)
                
            #CURRENTUNIXTIME = str(int(time.time()))

            return {"measurements": list(Measurements.values()), "time": int(time.time())}
'''
    @cherrypy.expose
    def weekData(self):
        return open('index.html')#
        '''
    
@cherrypy.expose
class TemperatureDatabaseWebService(object):#

    @cherrypy.tools.accept(media='text/plain')
    @cherrypy.tools.json_out()
    def GET(self):
        with sqlite3.connect(DB_STRING) as c:
            r = c.execute("SELECT * FROM room_temperature")
            temperatureData= r.fetchall()
            return temperatureData
        

    

def setup_database():
    """
    Create the `room_temperature` table in the database
    on server startup
    """
    pass


def cleanup_database():
    pass

if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/api': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }

    cherrypy.engine.subscribe('start', setup_database)
    #cherrypy.engine.subscribe('stop', cleanup_database)

    webapp = TemperatureDatabase()
    webapp.api = TemperatureDatabaseWebService()
    cherrypy.quickstart(webapp, '/', conf)

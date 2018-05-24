#import matplotlib.pyplot as plt
#from drawnow import drawnow
import sqlite3

'''
def make_fig():
    plt.scatter(x, y)  # I think you meant this

plt.ion()  # enable interactivity
fig = plt.figure()  # make a figure
'''

x = list()
y = list()


class Database:
    
    def __init__(self,File, tableName = 'Logging_Table'):
        self.database = sqlite3.connect(File)
        self.file = File
        self.tableName = tableName
        try:
            self.database.execute(
            #'''IF object_id("Logging_Table") is not null
                '''
                                    CREATE TABLE Logging_Table (
                                        TIME int,
                                        HUMIDITY int,
                                        CO2 int,
                                        TEMP int)
''')
        except sqlite3.OperationalError :
            print ("Logging_TableTable exists")
            cur = self.database.execute('SELECT COUNT(*) FROM Logging_Table;')
            data = cur.fetchone()
            print ("Current rows : %s" % data)    
            self.Close()
        else:
            self.Close()
        
    def Connect(self):
        self.database = sqlite3.connect(self.file)
        
        
    def LogEvent(self, Humidity = 0.0, CO2 = 0.0, Temp = 0.0):
        if (self.database == None):
            self.Connect()
            
        if (self.database != None):
            sql = "INSERT INTO "+self.tableName +" (TIME, HUMIDITY, CO2, TEMP) VALUES("+str(int(time.time()))+", "+str(int(Humidity))+", "+str(int(CO2))+", "+str(int(Temp))+");"
            print(sql)
            self.database.execute(sql)
            self.database.commit()
            #print("changes:", self.database.total_changes)
            self.Close()
            
    def Close(self):
        if (self.database != None):
            self.database.close()
            self.database = None


class DeviceIDs:
    Heater = 1
    Humidifier = 2
    Lights = 3
    Other = 4

from sense_hat import SenseHat

sense = SenseHat()
#from envirophat import weather
from sispmctl import SisPM
from sense_hat import SenseHat
RawData = []
import datetime
#sense = SenseHat()

#sense.show_message("Hello world!")
import time
device = SisPM(serial="01:01:57:5e:3c", binary="/usr/bin/sispmctl")

d = Database("Logging.db")

#for i in range(5):
try:
  while True:
    #print("Enviro Hat Temp",weather.temperature())
    print("Sense Hat Humdity", sense.humidity)
    print("Sense Hat Temp",sense.temperature)
    now = datetime.datetime.now()
    #print(now.hour)

    d.LogEvent(sense.humidity, 0, sense.temperature)
    x.append(now)
    y.append(sense.temperature)  # or any arbitrary update to your figure's data
    
    #drawnow(make_fig)
   
    if now.hour < 9 or now.hour > 15:
        device.on(DeviceIDs.Lights)
    else:
        device.off(DeviceIDs.Lights)
    #temperature range 21 to 35 degrees, 
    if sense.temperature < 25:
        device.on(DeviceIDs.Heater)
    else:
        device.off(DeviceIDs.Heater)


    #humidity = 50 to 70%
    if sense.humidity < 50:
        device.on(DeviceIDs.Humidifier)
    else:
        device.off(DeviceIDs.Humidifier)
    
    time.sleep(5)
    
except KeyboardInterrupt:
    print ("Shutdown requested...exiting")
    device.off(DeviceIDs.Lights)
    device.off(DeviceIDs.Heater)
    device.off(DeviceIDs.Humidifier)
    d.Close()
except Exception:
    device.off(DeviceIDs.Lights)
    device.off(DeviceIDs.Heater)
    device.off(DeviceIDs.Humidifier)
    d.Close()
    traceback.print_exc(file=sys.stdout)  

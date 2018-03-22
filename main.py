
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
import datetime
#sense = SenseHat()

#sense.show_message("Hello world!")
import time
device = SisPM(serial="01:01:57:5e:3c", binary="/usr/bin/sispmctl")
# get status of all outlets  
#device.get("all") # example result: {1: True, 2: True, 3: True, 4: True}
# turn on outlet 1

#for i in range(5):
while True:
    #print("Enviro Hat Temp",weather.temperature())
    print("Sense Hat Humdity", sense.humidity)
    print("Sense Hat Temp",sense.temperature)
    now = datetime.datetime.now()
    #print(now.hour)

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

    time.sleep(10)



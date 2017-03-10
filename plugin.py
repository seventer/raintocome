# Rain prediction plugin
#
# Author: Gerardvs
#
"""
<plugin key="FutureRainPlug" name="Rain Predictor Buienradar" author="gerardvs" version="1.0.3" wikilink="http://www.domoticz.com/wiki/plugins/plugin.html" externallink="http://www.buienradar.nl/overbuienradar/gratis-weerdata">
    <params>
        <param field="Mode1" label="DeviceID" width="125px" required="true" default="321H123U"/>
        <param field="Mode2" label="Emulate" width="75px">
            <options>
                <option label="True" value="Emulate"/>
                <option label="False" value="Normal"  default="true" />
            </options>
        </param>
        <param field="Mode3" label="Lookahead minutes" width="75px" required="true" default="45"/>
        <param field="Mode4" label="Update every x minutes" width="75px" required="true" default="15"/>
        <param field="Mode5" label="Value or mm" width="75px">
            <options>
                <option label="value" value="value"/>
                <option label="mm" value="mm"  default="mm" />
            </options>
        </param>
        <param field="Mode6" label="Debug" width="75px">
            <options>
                <option label="True" value="Debug"/>
                <option label="False" value="Normal"  default="true" />
            </options>
        </param>
    </params>
</plugin>
"""


import Domoticz
from rainfuture import RainFuture
from datetime import datetime, timedelta


lastUpdate = datetime.now()
location = ""


def onStart():
    global lastUpdate
    if Parameters["Mode6"] == "Debug":
            Domoticz.Debugging(1)
            Domoticz.Debug("onStart called")
            DumpConfigToLog()
    lastUpdate = datetime.now()
    CreateSensor()
    #DumpSettingsToLog()
    UpdateSensor()
    Domoticz.Heartbeat(30)
    return True


def onStop():
    Domoticz.Debug("onStop called")
    return True

def onConnect(Status, Description):
    Domoticz.Debug("onConnect called:")
    return True

def onMessage(Data, Status, Extra):
    Domoticz.Debug("onMessage called")
    return True

def onCommand(Unit, Command, Level, Hue):
    Domoticz.Debug("onCommand called")
    return True

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    Domoticz.Debug("onNotification called")
    return True

def onDisconnect():
    Domoticz.Debug("onDisconnect called")
    return True

def onHeartbeat():
    Domoticz.Debug("onHeartbeat called")
    interval = int(Parameters["Mode4"])
    if isActionTime(interval):
       UpdateSensor()



# Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device Idx:      '" + str(Devices[x].ID) + "'")
#        Domoticz.Debug("Device ID:       '" + Devices[x].DeviceID + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return

def DumpSettingsToLog():
    for x in Settings:
        if Settings[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Settings[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    return

def GetLocation():
    global location
    if Settings["Location"] != "":
        location = Settings["Location"].split(';')
        if (len(location)==2):
            Domoticz.Log( "'Lat':'" + location[0] + " Lon:" + location[1] + "'")
        else:
            LocationError()
    else:
        LocationError()
    
    return
        
        
def LocationError():        
        Domoticz.Error("Error reading location. Please enter the location coordinates in the system settings.")
        Domoticz.Error("Using default location. 52.09,5.11")
        location[0]="52.09"
        location[1]="5.11"


def CreateSensor():
    if (len(Devices) == 0):
       devID=Parameters["Mode1"]
       Domoticz.Device(Name="Rain2Come", Unit=1, TypeName="Custom",Used=1, DeviceID=devID).Create()
       Domoticz.Log("Rain2Come Device created")

def UpdateSensor():
    global lastUpdate
    global location
    nVal=0
    sVal=255
    
    if Parameters["Mode2"] == "Emulate":
        nVal = Devices[1].nValue
        nVal += 5
        if nVal>255:
            nVal=0
        sVal = 255 - nVal
    else:
        GetLocation()
        r = RainFuture()
        if Parameters["Mode6"] == "Debug":
            r.debug=True
        
        ahead = int(Parameters["Mode3"])
        
        if Parameters["Mode5"] == "value":
              nVal = r.getPredictionValue(location[0],location[1],ahead)
        else:
              nVal = r.getPrediction(location[0],location[1],ahead)
        
        sVal = nVal 
    
    Devices[1].Update(nVal,str(sVal))

    Domoticz.Log("Sensor updated: " + str(nVal) + ";" + str(sVal))
    Domoticz.Debug("Devices[1].Idx=" + str(Devices[1].ID))
    Domoticz.Debug("Devices[1].nValue=" + str(Devices[1].nValue))
    Domoticz.Debug("Devices[1].sValue=" + Devices[1].sValue)
    
    lastUpdate = datetime.now()


def isActionTime(minutes):
    nextUpdate = lastUpdate + timedelta(minutes=minutes)
    Domoticz.Debug("isActionTime:nextUpdate=" + str(nextUpdate))
    return datetime.now() > nextUpdate



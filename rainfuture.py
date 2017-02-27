#
# Rain prediction from Buienradar data
# shows maximum value within the coming n minutes
# Author: Gerard
#

import csv
import sys, math
import urllib.request
from datetime import datetime


class RainFuture:

    def __init__(self):
        self.debug = False

    #
    # Neerslagintensiteit = 10^((waarde-109)/32)
    # val2mm()
    # parameters:   value (0..255)
    # returns:      mm (rain in mm/hour)
    #
    def val2mm(self,rVal):
        return round(math.pow(10,((rVal-109)/32)),3)


    #
    # getRain()
    # parameters:   lat = lattitude
    #               lon = longitude
    # returns:      csv reader
    #
    def getRain(self,lat,lon):
        url = "http://gpsgadget.buienradar.nl/data/raintext?lat={}&lon={}".format(lat,lon)
        request = urllib.request.Request(url)
        with urllib.request.urlopen(request) as response:
             htpage = response.read().decode('utf-8').splitlines()

        return csv.reader(htpage, delimiter='|')


    #
    # getMaxmm()
    # parameters:  cr = csv.reader
    #              minutes = minutes ahead to check
    # returns:     max number of mm rain
    #
    def getMax(self,cr, minutes,do_value):
        max_val = 0
        lines = int(minutes/5)
        rowcount = 0
        for row in cr:
            rain_val = int(row[0])
            if (rain_val > max_val):
                max_val = rain_val
            rowcount += 1
            if (rowcount > lines):
                break

            if (self.debug):
                print ("rain_val=" + str(rain_val) + " time=" + row[1])
        retval = 0
        if (do_value==1):
           retval=max_val
        else:
           retval=self.val2mm(max_val)
        return retval

    def getPrediction(self,lat,lon,mins):
        cr = self.getRain(lat,lon)
        return self.getMax(cr,mins,0)

    def getPredictionValue(self,lat,lon,mins):
        cr = self.getRain(lat,lon)
        return self.getMax(cr,mins,1)


#
# main program
#
#r = RainFuture()
#r.debug=True
#aantal_mm = r.getPrediction("51.0","4.55",60)

#print("Total mm=" + str(aantal_mm) + " in the coming " + str(60) + " minutes")



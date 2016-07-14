#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Henning
#
# Created:     13.07.2016
# Copyright:   (c) Henning 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from collections import OrderedDict


class CL31day:
    """Class representing a whole day of records from the instrument.
    The class stores the raw data and contains methods for calculating stats."""

    def __init__(self, filename, data):
        self.filename = filename


        self.records = OrderedDict()

        #for t in range (0,len(data)): #Run until last row of file (EOF)
        for t in range (0,300): #Run until last row of file (EOF)

                      #Date,Type,Frag,CB1,CB2,CB3
            entries = [None,None,None,None,None,None]

            if data[t].startswith('Beginn:'): # IF "Beginn: is found within the entry
                #Date
                entries[0] = data[t][8:18]

                 #Time stamp = Dict Key!!!
                timestring = data[t][19:len(data[t])-1]
                time_stamp = tuple(timestring.split(":"))

                #Measurements
                status=data[t+2]    #Take next entry as
                #print status
                count=data[t+2][0]
                if(count=="0"): #Zero means no Cloudbase detected
                       entries[1] = "CLEAR"

                if(count=="1"): #one cloudbase
                    cloudbase=data[t+2][4:8]
                    #print cloudbase
                    entries[3] = cloudbase

                if(count=="2"): #two cloudbases
                    cloudbase=data[t+2][4:8]
                    #print cloudbase
                    entries[3] = cloudbase

                    cloudbase_t=data[t+2][10:14]
                    #print cloudbase_t
                    entries[4] = cloudbase_t

                if(count=="3"): # three cloudbases
                    cloudbase=data[t+2][4:8]
                    #print cloudbase
                    entries[3] = cloudbase
                    cloudbase_t=data[t+2][10:14]
                    #print cloudbase_t
                    entries[4] = cloudbase_t
                    cloudbase_g=data[t+2][16:20]
                    #print cloudbase_g
                    entries[5] = cloudbase_g

                if(count=="4"): # 4 in Fog (No cloudbase will be measured.... vertical visibility instead), Full obscuration
                   entries[1] = "FOG"
                   #print data[t+2]
                if(count=="5"): #5 in Fog (No cloudbase will be measured.... vertical visibility instead), Partly opaque
                    entries[1] = "FOG"
                    #print data[t+2]

                self.records[time_stamp] = entries


file = "d:\\Studium_EnvGEo\\Zweites_Semester\\Bendix\\Dev\\CL31msg2_20150101.txt"
with open(file, "r") as f:
   klasse = CL31day(file, f.readlines())

for k, v in klasse.records.items():
  print(k,v)
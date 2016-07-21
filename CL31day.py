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
import os

def ts_decode(time_stamp):
    """Function to convert tuple time stamp to
    elapsed seconds of the day (integer)."""
    s = int(time_stamp[2])
    ms = int(time_stamp[1]) * 60
    hs = int(time_stamp[0]) * 3600
    return(hs + ms + s)



class CL31day:
    """Class representing a whole day of records from the instrument.
    The class stores the raw data and contains methods for calculating stats."""

    #Class variables: Header information for various outputs
    #Records
    rec_fields = ("DATE", "TIME", "TYPE", "CLEAR_DIFF", "CB1", "CB2", "CB3")

    #Stats
    stats_meta = ("FILE","YEAR", "MONTH", "DAY")
    stats_fields = ("START", "END", "MEASUREMENTS", "CLEAR", "FO", "OPQ", "CD_MEDIAN", "CB1", "CB1_MIN", "CB1_MAX", "CB1_MEDIAN", "CB1_MODE", "CB2", "CB2_MEDIAN", "CB3", "CB3_MEDIAN")

    #Class Methods
    #Headerstring for file output
    def write_record_header(seperator=","):
        return seperator.join(rec_fields)

    #Headerstring for file output
    def write_stats_header(seperator=","):
        return seperator.join(CL31day.stats_meta + CL31day.stats_fields)



    def __init__(self, file, data):
        self.filename = os.path.basename(file)


        self.records = OrderedDict()

        for t in range (0,len(data)): #Run until last row of file (EOF)
##        for t in range (0,300): #Run until last row of file (EOF)

                      #Date,Type,Frag,CB1,CB2,CB3
            entries = [None,None,None,None,None,None]

            if data[t].startswith('Beginn:'): # IF "Beginn: is found within the entry
                #Date
                entries[0] = data[t][8:18]
                self.date = data[t][8:18]

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
                    entries[3] = int(cloudbase)

                if(count=="2"): #two cloudbases
                    cloudbase=data[t+2][4:8]
                    #print cloudbase
                    entries[3] = int(cloudbase)

                    cloudbase_t=data[t+2][10:14]
                    #print cloudbase_t
                    entries[4] = int(cloudbase_t)

                if(count=="3"): # three cloudbases
                    cloudbase=data[t+2][4:8]
                    #print cloudbase
                    entries[3] = int(cloudbase)
                    cloudbase_t=data[t+2][10:14]
                    #print cloudbase_t
                    entries[4] = int(cloudbase_t)
                    cloudbase_g=data[t+2][16:20]
                    #print cloudbase_g
                    entries[5] = int(cloudbase_g)

                if(count=="4"): # 4 in Fog (No cloudbase will be measured.... vertical visibility instead), Full obscuration
                   entries[1] = "FO"
                   #print data[t+2]
                if(count=="5"): #5 in Fog (No cloudbase will be measured.... vertical visibility instead), Partly opaque
                    entries[1] = "OPQ"
                    #print data[t+2]

                self.records[time_stamp] = entries



        #COMPUTE CLEAR DIFF
        clear_d = OrderedDict()
        for k, v in self.records.items():
            k_dec = ts_decode(k)
            if v[1] == "CLEAR":
                clear_d[k] = k_dec


        cld_keys = [k for k in clear_d.keys()]
##        print(cld_keys)
        for  x, k  in enumerate(cld_keys):
            if x + 1 >= len(cld_keys):
                break
            else:
                minuend = clear_d[cld_keys[x+1]]
                substrahend = clear_d[cld_keys[x]]
                diff = int(((minuend - substrahend)/20 -1))
                self.records[k][2] = diff



    def compute_stats(self, start=("00","00","00"), end=("23","59","59")):
        """Computes the statistics for the records and stores them as attributes."""

        #Class to contain the statistics
        class CL31stats:

            def median(collection):
                #calc median
                if len(collection) != 0:
                    collection.sort()
                    hl = (len(collection)//2)
                    if len(collection)%2 == 0:
                        return collection[hl-1]
                    elif len(collection)%2 == 1:
                        value = (collection[hl] + collection[hl-1])/2
                        return round(value)
                    else:
                        #Insert exception
                        return None
                else:
                    #list is empty
                    return None


            def __init__(self, types, cleardiff, cb1, cb2, cb3):

                #TIME WINDOW
                self.start = start
                self.end = end
                self.measurements = len(stat_dict)

                #TYPES
                self.clear = types.count("CLEAR")
                self.fo = types.count("FO")
                self.opq = types.count("OPQ")

                #CLEARDIFF
                self.cd_median = CL31stats.median(cleardiff)

                #CLOUDBASES
                #Count
                self.cb1 = len(cb1)
                self.cb2 = len(cb2)
                self.cb3 = len(cb3)

                #Median
                self.cb1_median = CL31stats.median(cb1)
                self.cb2_median = CL31stats.median(cb2)
                self.cb3_median = CL31stats.median(cb3)

                #Mode for CB1
                #count in dictionary
                counter = {}
                for cb in cb1:
                    if cb not in counter:
                        counter[cb] = 0
                    counter[cb] += 1

                #invert dictionary to find maximum
                counter = {v: k for k, v in counter.items()}
                #return maximum count as mode
                self.cb1_mode = counter[max(counter.keys())]

                #Minimum/Maximum for CB1
                self.cb1_min = min(cb1)
                self.cb1_max = max(cb1)


        #Get the relevant entries
        stat_dict = OrderedDict()
        for k,v in self.records.items():
            if ts_decode(start) <= ts_decode(k) <= ts_decode(end):
                stat_dict[k] = v

        #Convert to lists
        TYPES = []
        CLEARDIFF = []
        CB1 = []
        CB2 = []
        CB3 = []
        for v in stat_dict.values():
            TYPES.append(v[1])
            CLEARDIFF.append(v[2])
            CB1.append(v[3])
            CB2.append(v[4])
            CB3.append(v[5])
        #remove Nones
        TYPES = [v for v in TYPES if v != None]
        CLEARDIFF = [v for v in CLEARDIFF if v != None]
        CB1 = [v for v in CB1 if v != None]
        CB2 = [v for v in CB2 if v != None]
        CB3 = [v for v in CB3 if v != None]

        #Return the statistcs as an attribute
        self.stats = CL31stats(TYPES, CLEARDIFF, CB1, CB2, CB3)
        return



    #Return a seperated string of the attributes for file output
    def write_stat_string(self, seperator=","):
        #Get date elements from filename
        year = self.filename[9:13]
        month = self.filename[13:15]
        day = self.filename[15:17]

        #Convert complex elements to writable strings
        field_dict = {f: self.stats.__getattribute__(f.lower()) for f in CL31day.stats_fields}
        field_dict["START"] = ":".join(field_dict["START"])
        field_dict["END"] = ":".join(field_dict["END"])
        for  k, v in field_dict.items():
            print(v)
            if v == None:
                field_dict[k] = "NA"

        field_strings = [str(field_dict[f]) for f in CL31day.stats_fields]
        meta_strings = [self.filename, year, month, day]

        #Return the complete line
        return seperator.join(meta_strings + field_strings)















file = "d:\\Studium_EnvGEo\\Zweites_Semester\\Bendix\\Dev\\CL31msg2_20150101.txt"
with open(file, "r") as f:
   klasse = CL31day(file, f.readlines())

print(klasse.filename)
klasse.compute_stats()

output = "d:\\Studium_EnvGEo\\Zweites_Semester\\Bendix\\Dev\\stat_test.csv"
with open(output, "w") as out:
    out.write(CL31day.write_stats_header())
    out.write("\n")
    out.write(klasse.write_stat_string())


##start = ("00", "05", "00")
##
##end = ("01", "05", "00")
##
##clear_d = OrderedDict()
##for k, v in klasse.records.items():
##    k_dec = ts_decode(k)
##    if ts_decode(start) <= k_dec <= ts_decode(end):
##        if v[1] == "CLEAR":
##            clear_d[k] = k_dec
##
##
##cld_keys = [k for k in clear_d.keys()]
##print(cld_keys)
##for  x, k  in enumerate(cld_keys):
##    if x + 1 == len(cld_keys):
##        break
##    else:
##        minuend = clear_d[cld_keys[x+1]]
##        substrahend = clear_d[cld_keys[x]]
##        diff = int(((minuend - substrahend)/20 -1))
##        klasse.records[k][2] = diff

##for k, v in klasse.records.items():
##  print(k, v)







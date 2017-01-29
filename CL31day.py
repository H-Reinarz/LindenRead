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
    if type(time_stamp) == tuple:
        s = int(time_stamp[2])
        ms = int(time_stamp[1]) * 60
        hs = int(time_stamp[0]) * 3600
        return(hs + ms + s)
    elif type(time_stamp) == int:
        return(time_stamp)
    else:
        print("WRONG TIME STAMP")
        raise TypeError

def ts_encode(time_stamp):
    """Function to convert elapsed seconds of the day (integer)
    to tuple time stamp."""
    if type(time_stamp) == int:
        h = str(time_stamp//3600)
        mindiff = time_stamp % 3600
        minu = str(mindiff // 60)
        sec = str(mindiff % 60)
        t = [h, minu, sec]
        for n,x in enumerate(t):
            if len(x) == 1:
                t[n] = "0" + x
            else:
                pass
        return(tuple(t))

    elif type(time_stamp) == tuple:
        return(time_stamp)
    else:
        print("WRONG TIME STAMP")
        raise TypeError


class CL31day:
    """Class representing a whole day of records from the instrument.
    The class stores the raw data and contains methods for calculating stats."""

    #Class variables: Header information for various outputs
    #Records
    rec_fields = ("DATE", "TIME", "TYPE", "CLEAR_DIFF", "CB1", "CB2", "CB3")

    #Stats
    stats_meta = ("FILE","YEAR", "MONTH", "DAY")
    stats_fields = ("START", "END", "MEASUREMENTS", "CLEAR", "FO", "OPQ", "CD_MEDIAN", "CB1", "CB1_MIN", "CB1_MAX", "CB1_MEDIAN", "CB1_MODE", "CB2", "CB2_MEDIAN", "CB3", "CB3_MEDIAN")


    #Concentric Clears
    cc_fields = ('START_TIME', 'LIMIT', 'FM', 'FP', 'BM', 'BP')

    #Class Methods
    #Headerstring for file output
    def write_record_header(seperator=","):
        return seperator.join(rec_fields)

    #Headerstring for file output
    def write_stats_header(seperator=","):
        return seperator.join(CL31day.stats_meta + CL31day.stats_fields)

    #Headerstring for CC
    def write_cc_header(seperator=","):
        return seperator.join(CL31day.stats_meta + CL31day.cc_fields)



    def __init__(self, file, data):
        self.filename = os.path.basename(file)


        self.records = OrderedDict()

        for x, line in enumerate(data): #Run until last row of file (EOF)

            if line.__contains__("VS01") or len(line) > 30:
                continue

                      #Date,Type,Frag,CB1,CB2,CB3
            entries = [None,None,None,None,None,None]

            end = len(line) - 1
            if line.startswith('Beginn'): # IF "Beginn is found within the entry
                if line.startswith("Beginn: "):
                    stamp = line[8:end].split(" ")
                    date = stamp[0]
                else:
                    stamp = line[6:end]
                    if stamp.__contains__(" "):
                        stamp = stamp.split(" ")
                    else:
                        split = stamp.find(":")-2
                        stamp = [stamp[0:split], stamp[split:len(stamp)]]
                    date = stamp[0].split(".")
                    if len(date[2]) == 2:
                        year = str(int(date[2]) + 2000)
                        date[2] = year
                    date = ".".join(date)



                #Date
                entries[0] = date
                self.date = date
                 #Time stamp = Dict Key!!!
                time_stamp = tuple(stamp[1].split(":"))

                #Measurements
                status=data[x+2]    #Take next entry as
                #print status
                count=status[0]
                if(count=="0"): #Zero means no Cloudbase detected
                       entries[1] = "CLEAR"

                if(count=="1"): #one cloudbase
                    cloudbase=status[4:8]
                    #print cloudbase
                    entries[3] = int(cloudbase)

                if(count=="2"): #two cloudbases
                    cloudbase=status[4:8]
                    #print cloudbase
                    entries[3] = int(cloudbase)

                    cloudbase_t=status[10:14]
                    #print cloudbase_t
                    entries[4] = int(cloudbase_t)

                if(count=="3"): # three cloudbases
                    cloudbase=status[4:8]
                    #print cloudbase
                    entries[3] = int(cloudbase)
                    cloudbase_t=status[10:14]
                    #print cloudbase_t
                    entries[4] = int(cloudbase_t)
                    cloudbase_g=status[16:20]
                    #print cloudbase_g
                    entries[5] = int(cloudbase_g)

                if(count=="4"): # 4 in Fog (No cloudbase will be measured.... vertical visibility instead), Full obscuration
                   entries[1] = "FO"
                   #print status
                if(count=="5"): #5 in Fog (No cloudbase will be measured.... vertical visibility instead), Partly opaque
                    entries[1] = "OPQ"
                    #print status

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


    def records_generator(self, fields=[]):
        """Generator for iterating over a records dictionary. A subset of fields is selectable (default = all)."""
        for key, entries in self.records.items():
            if len(fields) != 0:
                subset = [entries[field] for field in fields]
            else:
                subset = entries
            yield key, subset

    def compute_clear_windows(self, start=("00","00","00"), end=("23","59","59"), duration=60, tolerance=2):
        """blub"""
        #Initialize clear window dictionary
        self.clear_windows = OrderedDict()

        #set up counter and function for generating window identifiers
        win_counter = 0
        make_win_id = lambda: "".join(reversed(self.date.split("."))) + "_" + str(win_counter).zfill(3)

        #Boolean functions for testing against maximum duration and tolerance of a window during loop
        max_dur = lambda clears, clouds: len(clears) + len(clouds) >= duration * 3
        max_tol = lambda clears, clouds: (len(cloud_count)/(duration * 3))*100 >= tolerance


        rec_iterator = self.records_generator(fields=1)
        for key, value in rec_iterator:
            value = value[0]

            if value == "CLEAR":
                begin = value
                clear_count = []
                clear_count.append(begin)
                cloud_count = []

                while begin:
                    sub_key, sub_value = next(rec_iterator)
                    sub_value = sub_value[0]

                    if sub_value == "CLEAR":
                        clear_count.append(sub_key)
                    else:
                        cloud_count.append(sub_key)

                    #Terminate the loop and save the window if appropriate
                    if max_dur(clear_count, cloud_count) or max_tol(clear_count, cloud_count):
                        if max_dur(clear_count, cloud_count):
                            win_counter += 1
                            #win_id = make_win_id()
                            self.clear_windows[make_win_id()] = [clear_count[0], sub_key]
                        break

            else:
                begin = None





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
                if len(cb1) != 0:
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
                else:
                    self.cb1_mode = None
                #Minimum/Maximum for CB1
                if len(cb1) != 0:
                    self.cb1_min = min(cb1)
                    self.cb1_max = max(cb1)
                else:
                    self.cb1_min = None
                    self.cb1_max = None



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
            #print(v)
            if v == None:
                field_dict[k] = "NA"

        field_strings = [str(field_dict[f]) for f in CL31day.stats_fields]
        meta_strings = [self.filename, year, month, day]

        #Return the complete line
        return seperator.join(meta_strings + field_strings)




    def compute_concentric_clears(self, start_time, limit):
        """blub"""
        class ConcentClears:
            def __init__(self, CL31d, st, lmt):
                self.start_time = st
                self.limit = lmt

                #FORWARD
                fm = 0
                fclouds = 0
                fp = 0

                for k,v in CL31d.records.items():
                    if not ts_decode(k) >= ts_decode(st):
                        continue
                    else:
                        fm += 1
                        if not v[1] == "CLEAR":
                            fclouds += 1
                        fp = round((fclouds/fm) * 100, ndigits=2)
                        if fp >= lmt:
                            break

                self.fm = fm
                self.fp = fp

                #BACKWARD
                rev_records = OrderedDict()
                for k in reversed(list(CL31d.records.keys())):
                    rev_records[k] = CL31d.records[k]

                bm = 0
                bclouds = 0
                bp = 0


                for k,v in rev_records.items():
                    if not ts_decode(k) <= ts_decode(st):
                        continue
                    else:
                        bm += 1
                        if not v[1] == "CLEAR":
                            bclouds += 1
                        bp = round((bclouds/bm) * 100, ndigits=2)
                        if bp >= lmt:
                            break


                self.bm = bm
                self.bp = bp


        #RETURN
        self.ConcentClears = ConcentClears(self, start_time, limit)



    #Return a seperated string of the attributes for file output
    def write_cc_string(self, seperator=","):
        #Get date elements from filename
        year = self.filename[9:13]
        month = self.filename[13:15]
        day = self.filename[15:17]

        #Convert complex elements to writable strings
        field_dict = {f: self.ConcentClears.__getattribute__(f.lower()) for f in CL31day.cc_fields}
        field_dict["START_TIME"] = ":".join(field_dict["START_TIME"])
        for  k, v in field_dict.items():
            #print(v)
            if v == None:
                field_dict[k] = "NA"

        field_strings = [str(field_dict[f]) for f in CL31day.cc_fields]
        meta_strings = [self.filename, year, month, day]

        #Return the complete line
        return seperator.join(meta_strings + field_strings)






#Test
file = "d:\\Studium_EnvGEo\\Zweites_Semester\\Bendix\\Dev\\CL31msg2_20150101.txt"
with open(file, "r") as f:
   klasse = CL31day(file, f.readlines())

klasse.compute_clear_windows()

##x = klasse.records_generator(fields=[1])
##
##print(klasse.date)
##
##for y in range(20):
##    key, value = next(x)
##    print(key)
##    print(value)


##
##print(klasse.filename)
##klasse.compute_stats()
##
##output = "d:\\Studium_EnvGEo\\Zweites_Semester\\Bendix\\Dev\\stat_test.csv"
##with open(output, "w") as out:
##    out.write(CL31day.write_stats_header())
##    out.write("\n")
##    out.write(klasse.write_stat_string())


##start_time = ('23', '39', '43')
##limit = 1
##
##m = 0
##clouds = 0
##perc = 0
##
##for k,v in klasse.records.items():
##    if not ts_decode(k) >= ts_decode(start_time):
##        continue
##    else:
##        m += 1
##        if not v[1] == "CLEAR":
##            clouds += 1
##        perc = round((clouds/m) * 100)
##        if perc >= limit:
##            break
##
##
##print("M:", m, "C:", clouds, "P:", perc)

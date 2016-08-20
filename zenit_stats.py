#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Henning
#
# Created:     04.08.2016
# Copyright:   (c) Henning 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import sys

sys.path.append("d:/Studium_EnvGEo/Zweites_Semester/Bendix/Dev/LindenRead")

from CL31day import *
from collections import OrderedDict

#Zenitzeiten
ZT = OrderedDict()
with open("d:/Studium_EnvGEo/Zweites_Semester/Bendix/Dev/AerosolZenith.bob") as zf:
    for line in zf.readlines():
        elements = line.split(";")
        ZT[elements[0]] = tuple(elements[1][:-1].split(":"))


time_window = 60



cl31_dir = "w:/Bendix/CL31/TEXT"


stats_file = "d:\\Studium_EnvGEo\\Zweites_Semester\\Bendix\\Dev\\CL31_stats_zenit_60.csv"

with open(stats_file, "w") as s:
    s.write(CL31day.write_stats_header() + ",ZENIT")
    s.write("\n")

    skipped = []
    for root, sub, files in os.walk(cl31_dir):
        base_dir = os.path.basename(root)
        print(base_dir)
        if  base_dir in ["2008", "2009", "2010", "2015", "2016"]:
            continue
        for file in files:
            filename = os.path.join(root, file)

            print(filename)
            with open(filename, "r") as raw:
                try:
                    raw_data = raw.readlines()
                except:
                    print("SKIPPED ", file, " !!!")
                    skipped.append(file)
                    continue

                #INitialize class
                Klasse = CL31day(filename, raw_data)

                #Set window for analyzing
                zenit = ts_decode(ZT[file[9:17]])
                start = ts_encode(zenit - round((time_window*60)/2))
                end = ts_encode(zenit + round((time_window*60)/2))

                #Analyze
##                print(file[-12:-4], ZT[file[-12:-4]], zenit, start, end, round((time_window*60)/2))
                Klasse.compute_stats(start, end)



                #Write
                s.write(Klasse.write_stat_string() + ","+":".join(ZT[file[9:17]]))
                s.write("\n")

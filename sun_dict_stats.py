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




sun_dict = {1: [('07', '20', '00'), ('15', '50', '00')],
            2: [('06', '37', '00'), ('16', '40', '00')],
            3: [('05', '35', '00'), ('17', '32', '00')],
            4: [('04', '30', '00'), ('18', '20', '00')],
            5: [('03', '36', '00'), ('19', '10', '00')],
            6: [('03', '15', '00'), ('19', '37', '00')],
            7: [('03', '32', '00'), ('19', '30', '00')],
            8: [('04', '15', '00'), ('18', '40', '00')],
            9: [('05', '00', '00'), ('17', '35', '00')],
            10: [('05', '50', '00'), ('16', '30', '00')],
            11: [('06', '40', '00'), ('15', '40', '00')],
            12: [('07', '20', '00'), ('15', '25', '00')]}


cl31_dir = "w:/Bendix/CL31/TEXT"

##stats_file = "d:\\Studium_EnvGEo\\Zweites_Semester\\Bendix\\Dev\\CL31_stats_2010-2016.csv"
##stats_file = "d:\\Studium_EnvGEo\\Zweites_Semester\\Bendix\\Dev\\CL31_stats_2010-2016_7-9.csv"
stats_file = "d:\\Studium_EnvGEo\\Zweites_Semester\\Bendix\\Dev\\CL31_stats_2008-2016.csv"
##stats_file = "d:\\Studium_EnvGEo\\Zweites_Semester\\Bendix\\Dev\\CL31_stats_2008-2016_7-9.csv"
##stats_file = "d:\\Studium_EnvGEo\\Zweites_Semester\\Bendix\\Dev\\CL31_stats_sun.csv"

with open(stats_file, "w") as s:
    s.write(CL31day.write_stats_header())
    s.write("\n")

    skipped = []
    for root, sub, files in os.walk(cl31_dir):
        base_dir = os.path.basename(root)
        print(base_dir)
##        if  base_dir == "2008" or base_dir == "2009":
##            continue
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

                #get sunrise and sunset times for the month
                month = int(file[13:15])
                srise = sun_dict[month][0]
                sset = sun_dict[month][1]

                Klasse = CL31day(filename, raw_data)
                Klasse.compute_stats(srise, sset)
##                Klasse.compute_stats(('07', '00', '00'), ('09', '00', '00'))
                s.write(Klasse.write_stat_string())
                s.write("\n")



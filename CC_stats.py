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


cc_limit = 1



cl31_dir = "w:/Bendix/CL31/TEXT"


stats_file = "d:\\Studium_EnvGEo\\Zweites_Semester\\Bendix\\Dev\\CL31_stats_cc_1.csv"

with open(stats_file, "w") as s:
    s.write(CL31day.write_cc_header())
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
                zenit = ZT[file[-12:-4]]

                #Analyze
                Klasse.compute_concentric_clears(zenit, cc_limit)

                #Write
                s.write(Klasse.write_cc_string())
                s.write("\n")

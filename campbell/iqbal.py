# Wird nach dem R Script campel1.R aufgerufen.
import calendar
import subprocess
from collections import OrderedDict

#### VARIABLES ####
# Inital File from iqbal
initalFile = r"H:/Geography/aerosol/iqbal_v2/initial.dat"
# Result File from iqbal
qtopo = r"H:/Geography/aerosol/iqbal_v2/qtopo.txt"
# CNR4 Table
fileDF = r"H:/Geography/aerosol/Data/zwischenergebnis/CNR4-2013.dat"
# Final Result (CNR4 Table with iqbal Value)
table = "H:/Geography/aerosol/Data/zwischenergebnis/CNR4-2013_iqbal.dat"

transDict = OrderedDict()


#### START ####
fDF = open(fileDF,"r")
# Iterate over every CNR4 Value
for index, DFlines in enumerate(fDF):
    #print(index)
    tmpList = []

    if index > 0:
        #### SEPERATE TIMESTAMP ####
        # Split by Seperator
        tmpDF = DFlines.split(";",1)
        # tmpDF[0] = Date; tmpDF[1] = All other columns
        # Seperate Date from Time:
        tmpDF = tmpDF[0].split(" ")
        date = tmpDF[0]
        time = tmpDF[1]
        
        # Stores Date(0 = Year, 1 = Month, 2 = Day)
        dateList = date.split("-")
        # Stores Time(0 = Year, 1 = Month, 2 = Day)
        timeList = time.split(":")
        
        # Store Day, Month, schaltjahr and time
        day = dateList[2]
        month = dateList[1]
        
        if calendar.isleap(int(dateList[0])):
            schaltjahr = "1"
        else:
            schaltjahr = "0"

        hour = timeList[0]
        minute = timeList[1]
        seconds = timeList[2]

        # Nullen eliminieren. "01" needs to be "1"
        if day[0] == "0":
            day = day[1]
        if month[0] == "0":
            month = month[1]
        if hour[0] == "0":
            if hour[1] == "0":
                hour = "0"
            else:
                hour = hour[1]
        if minute[0] == "0":
            if minute[1] == "0":
                minute = "0"
            else:
                minute = minute[1]
        if seconds[0] == "0":
            if seconds[1] == "0":
                seconds = "0"
            else:
                seconds = seconds[1]
        
        #### OPEN IQBAL ####
        f = open(initalFile,"r")
        for idx, lines in enumerate(f):
            
            # Day
            if idx ==  2: 
                tmpSplitList = lines.split('\t')
                lines = day + "\t" + tmpSplitList[1]
                tmpList.append(lines)
            # Month
            elif idx == 3:
                tmpSplitList = lines.split('\t')
                lines = month + "\t" + tmpSplitList[1]
                tmpList.append(lines)
            # Leap Year
            elif idx == 4:
                tmpSplitList = lines.split('\t')
                lines = schaltjahr + "\t" + tmpSplitList[1]
                tmpList.append(lines)
            #Time 
            elif idx == 5:
                tmpSplitList = lines.split('!')
                lines = hour + "  " + minute + "   " + seconds + "     !" + tmpSplitList[1]
                tmpList.append(lines)
            # Kill every Line greater than Line 19 (qtopo)
            elif idx > 19:
                pass
            # Append every other Line
            else:
                #tmpSplitList = lines.split('!')             
                #lines = tmpSplitList[0] + "!" + tmpSplitList[1]
                tmpList.append(lines)
        f.close()

        #### WRITE IQBAL ####
        # Write new lines to initalFile
        g = open(initalFile, 'w' ,) #encoding ='utf8')  

        # Write line by line
        for linesW in tmpList:
            g.write(linesW)
        g.close()	

        #### EXECUTE IQBAL ####
        cmd = 'H:/Geography/aerosol/iqbal_v2/iqbal_v2.exe'
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, cwd = "H:/Geography/aerosol/iqbal_v2")
        p.wait()
       
        #### READ RESULTS ####
        e = open(qtopo,"r")

        for rIdx, rLines in enumerate(e):
            if rIdx == 47:
                rLines = rLines.replace(" ","")
                rLines = rLines.split(":")
                radiationTAO = float(rLines[1])
            if rIdx == 49:
                rLines = rLines.replace(" ","")
                radiationGround = float(rLines)
            if rIdx == 54:
                rLines = rLines.replace(" ","")
                rLines = rLines.split(":")
                aerosolEffect = float(rLines[1])
        e.close()
        
        #### CALCULATE IQBAL RADIATION WITHOUT AEROSOL EFFECT
        radiation = (radiationTAO-aerosolEffect)+radiationGround
        transDict[date]=radiation
fDF.close()

w = open(table, 'w' ,) #encoding ='utf8')  

# Write line by line
w.write("Date;RadIqbal\n")
for key,value in transDict.items():

    #wVar = key,";",transDict[key]
    w.write(key)
    w.write(";")
    w.write(str(value))
    w.write("\n")

# Close file stream
w.close()	







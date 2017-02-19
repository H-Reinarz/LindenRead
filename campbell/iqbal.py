# Wird nach dem R Script campel1.R aufgerufen.
import calendar
import subprocess
from collections import OrderedDict
from time import gmtime, strftime

#### VARIABLES ####
# Inital File from iqbal
initalFile = r"H:/Geography/aerosol/iqbal_v2/initial.dat"
# Result File from iqbal
qtopo = r"H:/Geography/aerosol/iqbal_v2/qtopo.txt"
# CNR4 Table
fileDF = r"H:/Geography/aerosol/Data/zwischenergebnis2/CNR42012-2016_windows.csv"
# Final Result (CNR4 Table with iqbal Value)
table = "H:/Geography/aerosol/Data/zwischenergebnis2/ResultIqbal.csv"

transDict = OrderedDict()

print("Start: ")
strftime("%Y-%m-%d %H:%M:%S", gmtime())
print("\n")

#### START ####
fDF = open(fileDF,"r")
# Iterate over every CNR4 Value
for index, DFlines in enumerate(fDF):
    #print(index)
    tmpList = []

    if index == 0:
        head = DFlines

    if index > 0:
        #### SEPERATE TIMESTAMP ####
        # Split by Seperator
        tmpDF = DFlines.split(";",1)
        # tmpDF[0] = Date; tmpDF[1] = All other columns
        # Seperate Date from Time:
        tmpDF1 = tmpDF[0].split(" ")
        date = tmpDF1[0]
        time = tmpDF1[1]
        
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
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, cwd = "H:/Geography/aerosol/iqbal_v2", startupinfo=startupinfo)
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
        # Iqbalvalue; Timestamp(tmpDF1); other columns
        columns = str(radiation)+";"+tmpDF1[0]+" "+tmpDF1[1]+";"+str(tmpDF[1])
        transDict[index]=columns
fDF.close()

w = open(table, 'w' ,) #encoding ='utf8')  

# Write line by line
w.write("IqbalID;RadIqbal;")
w.write(head)
for key,value in transDict.items():

    #wVar = key,";",transDict[key]
    w.write(str(key))
    w.write(";")
    w.write(str(value))
    #w.write("\n")

# Close file stream
w.close()	

print("End: ")
strftime("%Y-%m-%d %H:%M:%S", gmtime())
print("\n")





# Wird nach dem R Script campel1.R aufgerufen.
import calendar
import subprocess


file = r"H:/Informatik/PythonApplications/iqbal/iqbal/initial.dat"
fileDF = r"h:/Geography/aerosol/Data/zwischenergebnis/CNR4-2013.dat"
fileResult = r"H:/Informatik/PythonApplications/iqbal/iqbal/qtopo.txt"
table = "h:/Geography/aerosol/Data/zwischenergebnis/CNR4-2013_iqbal.dat"

transDict = {}

fDF = open(fileDF,"r")

for index, DFlines in enumerate(fDF):
    
    dateList=[]
    timeList=[]

    print(index,"bob")

    if index > 0:
        tmpDF = DFlines.split(";",1)
        tmpDF = tmpDF[0].split(" ")
        date = tmpDF[0]
        time = tmpDF[1]
        
        dateList = date.split("-")
        timeList = time.split(":")

        day = dateList[2]
        month = dateList[1]
        
        if calendar.isleap(int(dateList[0])):
            schaltjahr = "1"
        else:
            schaltjahr = "0"


        hour = timeList[0]
        minute = timeList[1]
        seconds = timeList[2]

        # Nullen eliminieren
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

        f = open(file,"r")
        ###########################################
        tmpList = []

        for idx, lines in enumerate(f):
            
            if idx ==  2:
                tmpSplitList = lines.split('\t')
                lines = day + "\t" + tmpSplitList[1]
                tmpList.append(lines)
            elif idx == 3:
                tmpSplitList = lines.split('\t')
                lines = month + "\t" + tmpSplitList[1]
                tmpList.append(lines)
            elif idx == 4:
                tmpSplitList = lines.split('\t')
                lines = schaltjahr + "\t" + tmpSplitList[1]
                tmpList.append(lines)
            elif idx == 5:
                tmpSplitList = lines.split('!')
                lines = hour + "  " + minute + "   " + seconds + "     !" + tmpSplitList[1]
                tmpList.append(lines)
            elif idx > 19:
                pass
            else:
                #tmpSplitList = lines.split('!')             
                #lines = tmpSplitList[0] + "!" + tmpSplitList[1]
                tmpList.append(lines)


        f.close()

        # Write new lines to file
        # Open file stream
        g = open(file, 'w' ,) #encoding ='utf8')  

        # Write line by line
        for linesW in tmpList:

            g.write(linesW)

        # Close file stream
        g.close()	

        #subprocess.call("h:/Geography/aerosol/dir_aer/dir_aer.exe")
        cmd = 'H:/Informatik/PythonApplications/iqbal/iqbal/iqbal_v2.exe'
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        #for line in p.stdout:
        #    print (line)
        #Press('ENTER')
        p.wait()
        #Press('ENTER')
        #print (p.returncode)
        #p.kill

        e = open(fileResult,"r")

        for rIdx, rLines in enumerate(e):
            if rIdx == 47:
                l = []
                for t in rLines.split():
                    try:
                        l.append(float(t))
                    except ValueError:
                        pass

                bob = rLines

                transDict[date]=l[0]
        e.close()

      

fDF.close()

w = open(table, 'w' ,) #encoding ='utf8')  

 # Write line by line
for key,value in transDict.items():

    #wVar = key,";",transDict[key]
    w.write(key)
    w.write(";")
    w.write(str(value))
    w.write("\n")

# Close file stream
w.close()	







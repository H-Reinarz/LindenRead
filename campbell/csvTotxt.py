# Wandelt CSV-Dateien in txt um.
# Einige wenige Datensaetze der campbelldaten lagen als csv vor und musste dementsprechend angepasst werden.
import os
startpath = r"h:/Geography/aerosol/Data/linden/campbell/2013"


for file in os.listdir(startpath):
    if file.endswith("CNR4.csv"):
        print(file)
        tmpList = []
        filePath = startpath+"/"+file
        f = open(filePath,"r")
        
        tmpList.append("Custom Header\n")
        tmpList.append('"TIMESTAMP","RECORD","T_CNR_C_Avg","VIS_Up_Avg","VIS_Down_Avg","IR_Up_Avg","IR_Down_Avg","IR_Up_T_Avg","IR_Down_T_Avg","Rs_net_Avg","Rl_net_Avg","Rn_Avg","albedo_Avg","V_GND_Avg"\n')
        tmpList.append('"TS","RN","Deg C","W/m²","W/m²","W/m²","W/m²","W/m²","W/m²","W/m²","W/m²","W/m²","",""\n')
        tmpList.append('"","","Avg","Avg","Avg","Avg","Avg","Avg","Avg","Avg","Avg","Avg","Avg","Avg"        \n')

        
        
        for idx, line in enumerate(f):
            lineCheck = line.replace("-","")

            if idx == 0:
                pass
            elif idx == 1:
                firstLine = line
                tmpList.append(line)
            elif line == firstLine:
                break
            elif lineCheck[1:9] == file[0:8]:
                tmpList.append(line)
            else:
                pass
        f.close()

        newFile = filePath[:-4]+".txt"
        g = open(newFile, 'w' , encoding ='utf8')  

        # Write line by line
        for linesW in tmpList:

            g.write(linesW)
            #g.write("JA GE GE!")
            

        # Close file stream
        g.close()
            

        


#"TIMESTAMP","RECORD","T_CNR_C_Avg","VIS_Up_Avg","VIS_Down_Avg","IR_Up_Avg","IR_Down_Avg","IR_Up_T_Avg","IR_Down_T_Avg","Rs_net_Avg","Rl_net_Avg","Rn_Avg","albedo_Avg","V_GND_Avg"
#"TS","RN","Deg C","W/m²","W/m²","W/m²","W/m²","W/m²","W/m²","W/m²","W/m²","W/m²","",""
#"","","Avg","Avg","Avg","Avg","Avg","Avg","Avg","Avg","Avg","Avg","Avg","Avg"        

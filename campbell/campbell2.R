library(maptools)

# Pfad zu den Campbelldaten
path <- "h:/Geography/aerosol/Data/linden/campbell/"
YEARS <- list.dirs(path = "h:/Geography/aerosol/Data/linden/campbell/", full.names = F, recursive = F)
frameList <- list()
i <- 0
# Koordinaten der Lindenstation
lat.long <- matrix(c(8.683287899999982, 50.53348399999999), nrow = 1)



# Schleife, die alle *CNR4*.txt durchlaeuft, die Daten zum Zenithzeitpunkt extrahiert und in
# einen neuen Dataframe zusammenfuegt
for (year in YEARS){
  
  #year <- 2012
  # Zaehlvariable
  i <- i+1
  # Pfadvariable
  folderPath <- paste0(path,year,"/")
  # Files-Variable
  # ! Hier kann definiert werden, ob alle Jahre, oder ein spezifisches Jahr gesucht werden sollen !
  files <- list.files(folderPath, pattern = glob2rx(paste0(year,"*CNR4*.txt")), 
                      full.names = T)
  
  
  
  
  # lapply-Schleife die jede Zeile einer .txt durchlaeuft
  awb <- lapply(files, function(x){
    #x <- files[1]
    print(x)
    
    
    
    cnr <- read.table(x, sep=",", skip = 1, header=F)
    cnr <- cnr[!duplicated(cnr$V1),]
    cnr <- cnr[order(cnr$V2),]
    
    if(is.na(as.POSIXct(as.character(cnr[1,1]), zt = "UTC", format="%Y-%m-%d %H:%M:%S" ) )){
       colnames(cnr) <- as.character(unlist(cnr[1,]))
       cnr <- cnr[-1,]
       colnames(cnr)[1] <- "TIMESTAMP"
    } else{
      colnames(cnr)[1] <- "TIMESTAMP"
          
    }
    
    
    cnr$TIMESTAMP <- as.POSIXct(cnr$TIMESTAMP, format="%Y-%m-%d %H:%M:%S", tz = "UTC")
    cnr[, 2:ncol(cnr)] <- sapply(cnr[, 2:ncol(cnr)], as.numeric)
    
    fileName <- substr(basename(x),1,8)
    DATE <- as.Date(fileName, format = "%Y%m%d")
    MONTH <- as.numeric(format(DATE, format="%m"))
    
    day <- as.POSIXct(DATE, tz ="UTC")
    
    if(ncol(cnr)<14){
      cnr[,"V_GND_Avg"] <- -999
      
    }
    colnames(cnr) <- c("TIMESTAMP", "RECORD", "T_CNR_C_Avg", "VIS_Up_Avg", "VIS_Down_Avg", "IR_Up_Avg", "IR_Down_Avg", "IR_Up_T_Avg", "IR_Down_T_Avg", "Rs_net_Avg", "Rl_net_Avg", "Rn_Avg", "albedo_Avg", "V_GND_Avg")
    #print(colnames(cnr))
    # !!! AB HIER WIRD DER ZENITH BERECHNET !!!
    solarNoon <- solarnoon(lat.long, day, POSIXct.out=T)
    
    secondsToZero <- as.numeric(strftime(solarNoon$time, format = "%S"))
    solarNoon <- solarNoon$time - secondsToZero
    
    #   MONTH <- 1
    #   DATE <- "2016-03-27"
    
    # Monatsvariabilitaet der Tageslaengen
    if(MONTH == 1){
      subsetCNR <- cnr[cnr$TIMESTAMP >= as.POSIXct(paste0(DATE," 07:20:00"),format="%Y-%m-%d %H:%M:%S", tz = "UTC") 
                       & cnr$TIMESTAMP <= as.POSIXct(paste0(DATE," 15:50:00"),format="%Y-%m-%d %H:%M:%S", tz = "UTC"),]
    } else if(MONTH == 2){
      subsetCNR <- cnr[cnr$TIMESTAMP >= as.POSIXct(paste0(DATE," 06:37:00"),format="%Y-%m-%d %H:%M:%S", tz = "UTC") 
                       & cnr$TIMESTAMP <= as.POSIXct(paste0(DATE," 16:40:00"),format="%Y-%m-%d %H:%M:%S", tz = "UTC"),]
    } else if(MONTH == 3){
      subsetCNR <- cnr[cnr$TIMESTAMP >= as.POSIXct(paste0(DATE," 05:35:00"),format="%Y-%m-%d %H:%M:%S", tz ="UTC") 
                       & cnr$TIMESTAMP <= as.POSIXct(paste0(DATE," 17:32:00"),format="%Y-%m-%d %H:%M:%S", tz ="UTC"),]
    } else if(MONTH == 4){
      subsetCNR <- cnr[cnr$TIMESTAMP >= as.POSIXct(paste0(DATE," 04:30:00"),format="%Y-%m-%d %H:%M:%S", tz ="UTC") 
                       & cnr$TIMESTAMP <= as.POSIXct(paste0(DATE," 18:20:00"),format="%Y-%m-%d %H:%M:%S", tz ="UTC"),]
    } else if(MONTH == 5){
      subsetCNR <- cnr[cnr$TIMESTAMP >= as.POSIXct(paste0(DATE," 03:36:00"),format="%Y-%m-%d %H:%M:%S", tz ="UTC") 
                       & cnr$TIMESTAMP <= as.POSIXct(paste0(DATE," 19:10:00"),format="%Y-%m-%d %H:%M:%S", tz ="UTC"),]
    } else if(MONTH == 6){
      subsetCNR <- cnr[cnr$TIMESTAMP >= as.POSIXct(paste0(DATE," 03:15:00"),format="%Y-%m-%d %H:%M:%S", tz ="UTC") 
                       & cnr$TIMESTAMP <= as.POSIXct(paste0(DATE," 19:37:00"),format="%Y-%m-%d %H:%M:%S", tz ="UTC"),]
    } else if(MONTH == 7){
      subsetCNR <- cnr[cnr$TIMESTAMP >= as.POSIXct(paste0(DATE," 03:32:00"),format="%Y-%m-%d %H:%M:%S", tz ="UTC") 
                       & cnr$TIMESTAMP <= as.POSIXct(paste0(DATE," 19:30:00"),format="%Y-%m-%d %H:%M:%S", tz ="UTC"),]
    } else if(MONTH == 8){
      subsetCNR <- cnr[cnr$TIMESTAMP >= as.POSIXct(paste0(DATE," 04:15:00"),format="%Y-%m-%d %H:%M:%S", tz ="UTC") 
                       & cnr$TIMESTAMP <= as.POSIXct(paste0(DATE," 18:40:00"),format="%Y-%m-%d %H:%M:%S", tz ="UTC"),]
    } else if(MONTH == 9){
      subsetCNR <- cnr[cnr$TIMESTAMP >= as.POSIXct(paste0(DATE," 05:00:00"),format="%Y-%m-%d %H:%M:%S", tz ="UTC") 
                       & cnr$TIMESTAMP <= as.POSIXct(paste0(DATE," 17:35:00"),format="%Y-%m-%d %H:%M:%S", tz ="UTC"),]
    } else if(MONTH == 10){
      subsetCNR <- cnr[cnr$TIMESTAMP >= as.POSIXct(paste0(DATE," 05:50:00"),format="%Y-%m-%d %H:%M:%S", tz ="UTC") 
                       & cnr$TIMESTAMP <= as.POSIXct(paste0(DATE," 16:30:00"),format="%Y-%m-%d %H:%M:%S", tz ="UTC"),]
    } else if(MONTH == 11){
      subsetCNR <- cnr[cnr$TIMESTAMP >= as.POSIXct(paste0(DATE," 06:40:00"),format="%Y-%m-%d %H:%M:%S", tz ="UTC") 
                       & cnr$TIMESTAMP <= as.POSIXct(paste0(DATE," 15:40:00"),format="%Y-%m-%d %H:%M:%S", tz ="UTC"),]
    } else if(MONTH == 12){
      subsetCNR <- cnr[cnr$TIMESTAMP >= as.POSIXct(paste0(DATE," 07:20:00"),format="%Y-%m-%d %H:%M:%S", tz ="UTC") 
                       & cnr$TIMESTAMP <= as.POSIXct(paste0(DATE," 15:25:00"),format="%Y-%m-%d %H:%M:%S", tz ="UTC"),]
    } else{
      print("ERROR HA!")
    }
    
    # Erstellung neuer Spalten
    # Und Dekodierung von solarNoon (Zenith)
    subsetCNR$HOURS <- as.numeric(strftime(subsetCNR$TIMESTAMP, format="%H", tz ="UTC"))
    subsetCNR$MINUTES <- as.numeric(strftime(subsetCNR$TIMESTAMP, format="%M", tz ="UTC"))
    subsetCNR$SECONDS <- as.numeric(strftime(subsetCNR$TIMESTAMP, format="%S", tz ="UTC"))
    subsetCNR$TIMEDECODE <- subsetCNR$HOURS * 3600 + subsetCNR$MINUTES * 60 + subsetCNR$SECONDS
    subsetCNR$DAY <- as.numeric(strftime(subsetCNR$TIMESTAMP, format="%d", tz ="UTC"))
    subsetCNR$MONTH <- as.numeric(strftime(subsetCNR$TIMESTAMP, format="%m", tz ="UTC"))
    subsetCNR$YEAR <- as.numeric(strftime(subsetCNR$TIMESTAMP, format="%Y", tz ="UTC"))
    subsetCNR$DATE <- as.Date(strftime(subsetCNR$TIMESTAMP, format="%Y-%m-%d", tz ="UTC"))
    
    # Gebe die Zeile zurueck, in der die Zenithzeit steckt
    return(subsetCNR)
  })
  
  # Fuege alle Zenithzeiten jedes Tages zu einem Dataframe zusammen
  zenithFrame <- do.call("rbind", lapply(awb, function(x){data.frame(x)}))
  # Speichere den Dataframe in einer Liste (jedes Jahr = 1 Eintrag)
  frameList[[i]] <-zenithFrame
  
}

# Erstelle den finalen Dataframe mit der Zenithzeit von jedem Tag, in jedem Jahr
zenithFrame <- do.call("rbind", lapply(frameList, function(x){data.frame(x)}))



write.table(zenithFrame, "h:/Geography/aerosol/Data/zwischenergebnis2/CNR42012-2016.csv", row.names = F, quote = F, sep = ";")
# Plot
plot(zenithFrame$DATE, zenithFrame$TIMEDECODE)


lat.long <- matrix(c(8.683287899999982, 50.53348399999999), nrow = 1)



dateSeq <- seq(as.Date("2011-01-01"), as.Date("2014-12-31"), "days")
day <- as.POSIXct(dateSeq, tz ="UTC")
solarNoon <- solarnoon(lat.long, day, POSIXct.out=T)
bob <- strftime(solarNoon$time, format="", tz ="UTC")
bob <- gsub("-","",bob)
bob <- gsub(" ",";",bob)
#as.POSIXct(bob, tz ="UTC")
write.table(bob, "C:/geography/bendix/AerosolZenith.bob", row.names = F, col.names = F, quote = F)
?write.table

# 
# sun_dict = {1: [('07', '20', '00'), ('15', '50', '00')],
#   2: [('06', '37', '00'), ('16', '40', '00')],
#   3: [('05', '35', '00'), ('17', '32', '00')],
#   4: [('04', '30', '00'), ('18', '20', '00')],
#   5: [('03', '36', '00'), ('19', '10', '00')],
#   6: [('03', '15', '00'), ('19', '37', '00')],
#   7: [('03', '32', '00'), ('19', '30', '00')],
#   8: [('04', '15', '00'), ('18', '40', '00')],
#   9: [('05', '00', '00'), ('17', '35', '00')],
#   10: [('05', '50', '00'), ('16', '30', '00')],
#   11: [('06', '40', '00'), ('15', '40', '00')],
#   12: [('07', '20', '00'), ('15', '25', '00')]}
# 
# if(MONTH == 1){
#   start <- cnr$TIMESTAMP[cnr$TIMESTAMP == as.POSIXct(paste0(DATE," 07:20:00"),format="%Y-%m-%d %H:%M:%S", tz = "UTC")]
#   end <- cnr$TIMESTAMP[cnr$TIMESTAMP == as.POSIXct(paste0(DATE," 15:50:00"),format="%Y-%m-%d %H:%M:%S", tz = "UTC")]
#   subsetCNR <- cnr[cnr$TIMESTAMP >= start & cnr$TIMESTAMP <= end,]
# } else if(MONTH == 2){
#   start <- cnr$TIMESTAMP[cnr$TIMESTAMP == as.POSIXct(paste0(DATE," 06:37:00"),format="%Y-%m-%d %H:%M:%S", tz = "UTC")]
#   end <- cnr$TIMESTAMP[cnr$TIMESTAMP == as.POSIXct(paste0(DATE," 16:40:00"),format="%Y-%m-%d %H:%M:%S", tz = "UTC")]
#   subsetCNR <- cnr[cnr$TIMESTAMP >= start & cnr$TIMESTAMP <= end,]
# } else if(MONTH == 3){
#   start <- cnr$TIMESTAMP[cnr$TIMESTAMP == as.POSIXct(paste0(DATE," 05:35:00"),format="%Y-%m-%d %H:%M:%S", tz ="UTC")]
#   end <- cnr$TIMESTAMP[cnr$TIMESTAMP == as.POSIXct(paste0(DATE," 17:32:00"),format="%Y-%m-%d %H:%M:%S", tz ="UTC")]
#   subsetCNR <- cnr[cnr$TIMESTAMP >= start & cnr$TIMESTAMP <= end,]
# } else if(MONTH == 4){
#   start <- cnr$TIMESTAMP[cnr$TIMESTAMP == as.POSIXct(paste0(DATE," 04:30:00"),format="%Y-%m-%d %H:%M:%S", tz ="UTC")]
#   end <- cnr$TIMESTAMP[cnr$TIMESTAMP == as.POSIXct(paste0(DATE," 18:20:00"),format="%Y-%m-%d %H:%M:%S", tz ="UTC")]
#   subsetCNR <- cnr[cnr$TIMESTAMP >= start & cnr$TIMESTAMP <= end,]
# } else if(MONTH == 5){
#   start <- cnr$TIMESTAMP[cnr$TIMESTAMP == as.POSIXct(paste0(DATE," 03:36:00"),format="%Y-%m-%d %H:%M:%S", tz ="UTC")]
#   end <- cnr$TIMESTAMP[cnr$TIMESTAMP == as.POSIXct(paste0(DATE," 19:10:00"),format="%Y-%m-%d %H:%M:%S", tz ="UTC")]
#   subsetCNR <- cnr[cnr$TIMESTAMP >= start & cnr$TIMESTAMP <= end,]
# } else if(MONTH == 6){
#   start <- cnr$TIMESTAMP[cnr$TIMESTAMP == as.POSIXct(paste0(DATE," 03:15:00"),format="%Y-%m-%d %H:%M:%S", tz ="UTC")]
#   end <- cnr$TIMESTAMP[cnr$TIMESTAMP == as.POSIXct(paste0(DATE," 19:37:00"),format="%Y-%m-%d %H:%M:%S", tz ="UTC")]
#   subsetCNR <- cnr[cnr$TIMESTAMP >= start & cnr$TIMESTAMP <= end,]
# } else if(MONTH == 7){
#   start <- cnr$TIMESTAMP[cnr$TIMESTAMP == as.POSIXct(paste0(DATE," 03:32:00"),format="%Y-%m-%d %H:%M:%S", tz ="UTC")]
#   end <- cnr$TIMESTAMP[cnr$TIMESTAMP == as.POSIXct(paste0(DATE," 19:30:00"),format="%Y-%m-%d %H:%M:%S", tz ="UTC")]
#   subsetCNR <- cnr[cnr$TIMESTAMP >= start & cnr$TIMESTAMP <= end,]
# } else if(MONTH == 8){
#   start <- cnr$TIMESTAMP[cnr$TIMESTAMP == as.POSIXct(paste0(DATE," 04:15:00"),format="%Y-%m-%d %H:%M:%S", tz ="UTC")]
#   end <- cnr$TIMESTAMP[cnr$TIMESTAMP == as.POSIXct(paste0(DATE," 18:40:00"),format="%Y-%m-%d %H:%M:%S", tz ="UTC")]
#   subsetCNR <- cnr[cnr$TIMESTAMP >= start & cnr$TIMESTAMP <= end,]
# } else if(MONTH == 9){
#   start <- cnr$TIMESTAMP[cnr$TIMESTAMP == as.POSIXct(paste0(DATE," 05:00:00"),format="%Y-%m-%d %H:%M:%S", tz ="UTC")]
#   end <- cnr$TIMESTAMP[cnr$TIMESTAMP == as.POSIXct(paste0(DATE," 17:35:00"),format="%Y-%m-%d %H:%M:%S", tz ="UTC")]
#   subsetCNR <- cnr[cnr$TIMESTAMP >= start & cnr$TIMESTAMP <= end,]
# } else if(MONTH == 10){
#   start <- cnr$TIMESTAMP[cnr$TIMESTAMP == as.POSIXct(paste0(DATE," 05:50:00"),format="%Y-%m-%d %H:%M:%S", tz ="UTC")]
#   end <- cnr$TIMESTAMP[cnr$TIMESTAMP == as.POSIXct(paste0(DATE," 16:30:00"),format="%Y-%m-%d %H:%M:%S", tz ="UTC")]
#   subsetCNR <- cnr[cnr$TIMESTAMP >= start & cnr$TIMESTAMP <= end,]
# } else if(MONTH == 11){
#   start <- cnr$TIMESTAMP[cnr$TIMESTAMP == as.POSIXct(paste0(DATE," 06:40:00"),format="%Y-%m-%d %H:%M:%S", tz ="UTC")]
#   end <- cnr$TIMESTAMP[cnr$TIMESTAMP == as.POSIXct(paste0(DATE," 15:40:00"),format="%Y-%m-%d %H:%M:%S", tz ="UTC")]
#   subsetCNR <- cnr[cnr$TIMESTAMP >= start & cnr$TIMESTAMP <= end,]
# } else if(MONTH == 12){
#   start <- cnr$TIMESTAMP[cnr$TIMESTAMP == as.POSIXct(paste0(DATE," 07:20:00"),format="%Y-%m-%d %H:%M:%S", tz ="UTC")]
#   end <- cnr$TIMESTAMP[cnr$TIMESTAMP == as.POSIXct(paste0(DATE," 15:25:00"),format="%Y-%m-%d %H:%M:%S", tz ="UTC")]
#   subsetCNR <- cnr[cnr$TIMESTAMP >= start & cnr$TIMESTAMP <= end,]
# } else{
#   print("ERROR HA!")
# }
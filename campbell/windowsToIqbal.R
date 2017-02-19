windows <- read.csv("H:/Geography/aerosol/Data/Windows/CL31_CW_2012-2014.csv")
cnrvalues <- read.csv("H:/Geography/aerosol/Data/zwischenergebnis2/CNR42012-2016.csv", sep=";")


# Add date to windows data.frame
for(i in seq(1:nrow(windows))){
  windows$DATE[i] <- as.Date(paste0(windows$YEAR[i],"-",windows$MONTH[i],"-",windows$DAY[i]))
}
windows$DATE <- as.Date(windows$DATE, origin='1970-01-01 00:00.00 UTC')

for(i in seq(1:nrow(windows))){
  windows$DATE_START[i] <- as.POSIXct(strptime(paste0(windows$YEAR[i],"-",windows$MONTH[i],"-",windows$DAY[i]," ",as.character(windows$BUFF_START[i])), "%Y-%m-%d %H:%M:%S"))
}
windows$DATE_START <- as.POSIXct(windows$DATE_START, origin='1970-01-01 00:00.00 UTC')

for(i in seq(1:nrow(windows))){
  windows$DATE_END[i] <- as.POSIXct(strptime(paste0(windows$YEAR[i],"-",windows$MONTH[i],"-",windows$DAY[i]," ",as.character(windows$BUFF_END[i])), "%Y-%m-%d %H:%M:%S"))
}
windows$DATE_END <- as.POSIXct(windows$DATE_END, origin='1970-01-01 00:00.00 UTC')

# Add date to cnrvalues data.frame
cnrvalues$DATE <- as.Date(cnrvalues$DATE)

##################################################



dates <- unique(cnrvalues$DATE)
result <- 0
for(i in seq(1:nrow(windows))){
 #i<-401
  if(!(windows$DATE[i] %in% dates)){
    
  } else{
    cnrWin <- subset(cnrvalues, cnrvalues$DATE == windows$DATE[i])
    for(j in seq(1:nrow(cnrWin))){
      cnrWin$POSTIME[j] <- as.POSIXct(strptime(as.character(cnrWin$TIMESTAMP[j]), "%Y-%m-%d %H:%M:%S"))
    }
    cnrWin$POSTIME <- as.POSIXct(cnrWin$POSTIME, origin='1970-01-01 00:00.00 UTC')
    cnrWin <- subset(cnrWin, cnrWin$POSTIME <= windows$DATE_END[i] & cnrWin$POSTIME >= windows$DATE_START[i])
    
    cnrWin$ID <- windows$ID[i]
    cnrWin <- cbind(cnrWin, windows[i,10:13])
    
    if(is.data.frame(result)){
      result <- rbind(result, cnrWin)
    } else{
      result <- cnrWin
    }
  }


}

result$SECONDS <- NULL
result$TIMEDECODE <- NULL
result$POSTIME <- NULL
write.table(result, "h:/Geography/aerosol/Data/zwischenergebnis2/CNR42012-2016_windows.csv", row.names = F, quote = F, sep = ";")
length(unique(result$ID))

# for(i in seq(1:nrow(cnrvalues))){
#   cnrvalues$POSTIME[i] <- as.POSIXct(strptime(as.character(cnrvalues$TIMESTAMP[i]), "%Y-%m-%d %H:%M:%S"))
# }
# cnrvalues$POSTIME <- as.POSIXct(cnrvalues$POSTIME, origin='1970-01-01 00:00.00 UTC')
# 
# for(i in seq(1:nrow(windows))){
#   windows$DATE_START[i] <- as.POSIXct(strptime(paste0(windows$YEAR[i],"-",windows$MONTH[i],"-",windows$DAY[i]," ",as.character(windows$BUFF_START[i])), "%Y-%m-%d %H:%M:%S"))
# }
# windows$DATE_START <- as.POSIXct(windows$DATE_START, origin='1970-01-01 00:00.00 UTC')
# 
# for(i in seq(1:nrow(windows))){
#   windows$DATE_END[i] <- as.POSIXct(strptime(paste0(windows$YEAR[i],"-",windows$MONTH[i],"-",windows$DAY[i]," ",as.character(windows$BUFF_START[i])), "%Y-%m-%d %H:%M:%S"))
# }
# windows$DATE_END <- as.POSIXct(windows$DATE_END, origin='1970-01-01 00:00.00 UTC')
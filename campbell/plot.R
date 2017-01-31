cnr4 <- read.table("h:/Geography/aerosol/Data/zwischenergebnis/CNR4-2013.dat", sep = ";", header = T)
iqbal <- read.table("h:/Geography/aerosol/Data/zwischenergebnis/CNR4-2013_iqbal.dat", sep = ";", header = T)

plot(seq(1:nrow(cnr4)), iqbal$RadIqbal, type = "p", cex = .5, col="#542788", pch = 16)
plot(seq(1:nrow(cnr4)), cnr4$VIS_Up_Avg, type = "p", cex = .5, col="#542788", pch = 16)
?plot

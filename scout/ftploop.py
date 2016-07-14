from ftplib import FTP
import tarfile
from io import BytesIO

ftp = FTP('')     
ftp.login("","")
ftp.pwd()
print(ftp.pwd())

# FTP Class
class FTPList:

    def __init__(self, instr, years="all", months="all", days="all"):
        self.instr = instr
        self.years = years
        self.months = months
        self.days = days
        
        
        
    def ShowYears(self):
        ftp.cwd(self.instr)
        ftp.retrlines('LIST')
        ftp.cwd("/")
    
    def GetList(self):

        dic = {}
        yearList = []
        fileList = []
        
        if self.years == "all":
            ftp.cwd(self.instr)
            
            yearList = ftp.nlst()

            for yeari in yearList:
                dic[yeari] = []
                ftp.cwd(yeari)
                dic[yeari] = ftp.nlst()
                ftp.cwd("/"+self.instr)
                
            
            return (dic)

# Run
klasse = FTPList("cl31")
cl31Dic = klasse.GetList()


# Test Run for all days of 2014
ftp.cwd("2014")
for fileArchive in cl31Dic["2014"]:
    f = BytesIO()
    theFile = ftp.retrbinary("RETR "+fileArchive,f.write)
    f.seek(0)
    tar = tarfile.open(fileobj=f)
    
    t = tar.extractfile(tar.getmembers()[0])
    data = [x.decode("utf_8") for x in t.readlines()]

    #Test
    print(fileArchive)
    print(data[0:5])
    

# Original Loop
##for years in cl31Dict:
##        
##    for fileArchive in years:
##        f = BytesIO()
##        theFile = ftp.retrbinary("RETR "+fileArchive,f.write)
##        f.seek(0)
##        tar = tarfile.open(fileobj=f)
##        
##        t = tar.extractfile(tar.getmembers()[0])
##        data = [x.decode("utf_8") for x in t.readlines()]

		
		

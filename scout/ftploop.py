from ftplib import FTP
import tarfile
from io import BytesIO


ftp = FTP('')     
ftp.login("","")
ftp.pwd()
print(ftp.pwd())

class FTPList:

    def __init__(self, instr, years="all", months="all", days="all"):
        self.instr = instr
        self.years = years
        self.months = months
        self.days = days
        
        
        
    def ShowYears(self):
        ftp.cwd(self.instr)
        ftp.retrlines('LIST')
    
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
        
            


		
		
		
# Old Code
#f = BytesIO()

#theFile = ftp.retrbinary("RETR CL31msg2_20081231.txt.tar",f.write)

#f.seek(0)

#tar = tarfile.open(fileobj=f)

#for member in tar.getmembers():
    #t = tar.extractfile(member)
    #data = [x.decode("utf_8") for x in t.readlines()]
    #for x in range(0,11):
     #   print(data[x])


#ftp.close()



#
#
#

from ftplib import FTP
import tarfile
from io import BytesIO


ftp = FTP('')     # connect to host, default port
ftp.login("","")                     # user anonymous, passwd anonymous@

ftp.cwd('cl31')               # change into "debian" directory
ftp.retrlines('LIST')           # list directory contents
ftp.cwd('2008')

f = BytesIO()

theFile = ftp.retrbinary("RETR CL31msg2_20081231.txt.tar",f.write)

f.seek(0)

tar = tarfile.open(fileobj=f)

for member in tar.getmembers():
    t = tar.extractfile(member)
    data = [x.decode("utf_8") for x in t.readlines()]

    for x in range(0,11):
        print(data[x])


ftp.close()



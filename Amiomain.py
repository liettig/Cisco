from Amiossh import NetworkDevice
from Amioutil import print_device_info
from Amioutil import read_devices_info
import getpass
import sys
from datetime import datetime
import logging
import os # for prne.log file removal if exists

#file csv da cui leggo la lista dei device
#####devices_filename = 'CorsoENARSI/S1ImplementingEIGRP/S15csv-devices'
#file di log -> prne.log
filedir = os.path.dirname(__file__)
logfile = os.path.join(filedir, 'Amio.log')

#cancelliamo, se esiste, prne.log altrimenti logging.basicConfig fa l'append ogni volta
try:
    os.remove(logfile)
except:
    print("Error while deleting file ", logfile)

#questa linea indica che verranno visualizzati i messaggi di log di paramiko (solo se sono WARNING o superiori)
logging.getLogger("paramiko").setLevel(logging.WARNING)
#formato base delle colonne che trovero' nel file prne.log 
logging.basicConfig(filename=logfile,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    level=logging.INFO)

username = input('username: ')
while username == '':
    username = input('username: ')
password = getpass.getpass()

device = NetworkDevice(username,password)
device.templateConfig()




    

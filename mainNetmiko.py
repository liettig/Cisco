from devclassNetmiko import NetworkDevice
from utilNetmiko import print_device_info
from utilNetmiko import read_devices_info
import getpass
import sys
from datetime import datetime
import logging
import os # for prne.log file removal if exists

filedir = os.path.dirname(__file__)
devices_filename = os.path.join(filedir, 'csv-devices')

#file di log -> prne.log
logfile = 'prne.log'

#cancelliamo, se esiste, prne.log altrimenti logging.basicConfig fa l'append ogni volta
try:
    os.remove(logfile)
except:
    print("Error while deleting file ", logfile)

# the following line to write paramiko log messages (only if WARNING higher level)
logging.getLogger("paramiko").setLevel(logging.WARNING)
#column base format in prne.log file
logging.basicConfig(filename='prne.log',
                    format='%(asctime)s %(levelname)s: %(message)s',
                    level=logging.INFO)

devices_list_in = read_devices_info(devices_filename)  

logging.info('mainNetmiko: read %s devices from file %s', len(devices_list_in), devices_filename)

# Iterate through all devices from the file, creating device objects for each

# *** device_in
# *** ['eng-lab-ch-bel-r-005', 'IOS-XE', '10.0.224.25', 'admin', 't1c1n0']
username = input('username: ')
while username == '':
    username = input('username: ')
password = getpass.getpass()
for device_in in devices_list_in:
    ##device = NetworkDevice('eng-lab-ch-bel-s-001', '10.0.224.31', user = username, pw = password)

    device = NetworkDevice(device_in[0],  # Device name         var: name
                           device_in[2],  # Device IP address   var: ip_address
                           username,
                           password)
    
    start_msg = '===> {} Connection to: {}'
    #received_msg = '<=== {} Received from:   {}'
    logging.info(start_msg.format(datetime.now().time(), device.ip_address))

    device.connect()
    #received_msg = '<=== {} Received from:   {}'
    device.get_interfaces()
    if device.name == 'eng-lab-ch-bel-s-001':
        device.templateInt()
    elif device.name == 'eng-lab-ch-bel-s-002':
        device.multiple_commands()
    else:
        pass
        

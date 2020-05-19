import csv
from pprint import pprint
from Amiossh import NetworkDevice
import logging

#======================================================================
def read_devices_info(devices_file):

    ###devices_list = []

    logging.info('printutilnetmiko: reading device info from file: %s', devices_file)

    file = open(devices_file,'r')   # Open the CSV file
    csv_devices = csv.reader(file)  # Create the CSV reader for file

    # Use list comprehension to put CSV data into list of lists
    #ritorna [
    #           ['eng-lab-ch-bel-r-005', 'IOS-XE', '10.0.224.25', 'admin', 't1c1n0'],
    #           ['eng-lab-ch-bel-s-001', 'IOS', '10.0.224.31', 'admin', 't1c1n0'], 
    #           ['eng-lab-ch-bel-s-002', 'IOS', '10.0.224.32', 'admin', 't1c1n0']
    #          ]
    return [dev_info for dev_info in csv_devices]



#====================================================================
def print_device_info(device):

    #print ('-------------------------------------------------------')
    #print ('    Device Name:      ',device.name)
    #print ('    Device IP:        ',device.ip_address)
    print ('---------------------------------------------------------')
    print('--- show interfaces summary --- \n {}'.format(device.interfaces))
    #print(device.output)
    #print ('------------------ show ip route ----------------------')
    #print(device.show)
    #print (device.interfaces)
    #print (device.result)


#====================================================================

def write_devices_info(devices_file, devices_out_list):

    logging.info('util: writing device info to file: %s', devices_file)

    # Use CSV library to output our list of lists to a CSV file
    with open(devices_file, 'w') as file:
        csv_out = csv.writer(file)
        csv_out.writerows(devices_out_list)
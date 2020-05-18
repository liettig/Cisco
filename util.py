import devclass
from pprint import pprint

#======================================================================
def read_devices_info(devices_file):

    devices_list = []

    file = open(devices_file,'r')
    for line in file:

        device_info = line.strip().split(',')

        # Create a device object with this data
        if device_info[1] == 'IOS':

            device = devclass.NetworkDeviceIOS(device_info[0],device_info[2],
                                      device_info[3],device_info[4])
            
        else:
            device = devclass.NetworkDevice(device_info[0],device_info[2],
                                   device_info[3],device_info[4])

        devices_list.append(device)

    return devices_list


#====================================================================
def print_device_info(device):

    print ('-------------------------------------------------------')
    print ('    Device Name:      ',device.name)
    print ('    Device IP:        ',device.ip_address)
    print ('    Device username:  ',device.username)
    print ('    Device password:  ',device.password)

    print ('')
    print ('    Interfaces')
    print ('')

    pprint (device.interfaces)
    print ('-------------------------------------------------------\n\n')


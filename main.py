import util

#====================================================================
# Main program: connect to device, show interface, display

devices_list = util.read_devices_info('devices.txt')

for device in devices_list:

    print ('==== Device =============================================================')

    device.connect()
    device.get_interfaces()
    util.print_device_info(device)


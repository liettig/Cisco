import pexpect
from getpass import getpass

#-----------------------------------------------------------
# The following code connects to a device

def connect(dev_ip,username,password):
    """
    Connects to device using pexpect

    :dev_ip: The IP address of the device we are connectin to
    :username: The username that we should use when logging in
    :password: The password that we should use when logging in

    =return: pexpect session object if succssful, 0 otherwise

    """

    print ('--- attempting to: ssh ' + dev_ip)

    session = pexpect.spawn('ssh ' + username + '@' + dev_ip, timeout=5)
    result = session.expect(['Password:', pexpect.TIMEOUT])

    # Check for failure
    if result != 0:
        print ('--- Timeout or unexpected reply from device')
        return 0
    else:
        print('SSH connection SUCCESSFUL')
    print ('--- attempting to login: ')

    # Session expecting password, enter it here
    session.sendline(password)
    result = session.expect(['#', pexpect.TIMEOUT])

    # Check for failure
    if result != 0:
        print (' FAILURE! entering password: '), password
        return 0
    else:
        print('login SUCCESSFUL')
    return session  # return pexpect session object to caller

#-----------------------------------------------------------
# The following function gets and returns interface information

def show_int_summary(session):
    """
    Runs 'show int summary' command on device and returns 
    output from device in a string

    session: The pexpect session for communication with device

    return: string of output from device
    """

    print ('--- show interface summary command')
    session.sendline('show interface summary')
    result = session.expect(['#', pexpect.TIMEOUT, pexpect.EOF])

    print ('--- getting interface command output')
    show_int_sum_output = session.before

    return show_int_sum_output

#------------------------------------------------------------
# Main program: connect to device, show interface, display

if __name__ == '__main__':

    rtrip = input('enter rtr ip address: ')
    rtruser = input('enter rtr username: ')
    rtrpass = getpass('enter rtr password: ')
    
    session = connect(rtrip,rtruser,rtrpass)
    if session == 0:
        print ('--- Session attempt unsuccessful, exiting.')
        exit()

    output_data = show_int_summary(session)

    print ('')
    print ('Show Interface Output')
    print ('-----------------------------------------------------')
    print ('')

    print (output_data)

    session.sendline('quit')
    session.close()
    session.kill(0)




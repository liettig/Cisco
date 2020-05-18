import paramiko
from pprint import pprint
from getpass import getpass

#-----------------------------------------------------------
# The following code connects to a device

def connect(ip_address,username,password):
    """
    Connects to device using paramiko

    :ip_address: The IP address of the device we are connectin to
    :username: The username that we should use when logging in
    :password: The password that we should use when logging in

    =return: paramiko session object if succssful

    """

    print ('\n------------------------------------------------------')
    print ('--- Attempting paramiko connection to: ', ip_address)

    # Create paramiko session
    ssh_client = paramiko.SSHClient()

    # Must set missing host key policy since we don't have the SSH key
    # stored in the 'known_hosts' file
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Make the connection to our host.
    ssh_client.connect(hostname=ip_address,
                       username=username,
                       password=password)
    
    return ssh_client


########## comandi per veedere se la funzione ritornata è corretta ##########
#ssh = connect('10.0.224.25','admin','t1c1n0')
#stdin, stdout, stderr = ssh.exec_command('show ip route')
#ip_route_table = stdout.readlines()
#pprint (ip_route_table)
#ssh.close()
##############################################################################

#-----------------------------------------------------------
# The following function gets and returns interface information

def show_ip_route(ssh_client):

    stdin, stdout, stderr = ssh_client.exec_command('show ip route')
    ip_route_table = stdout.readlines()
    return ip_route_table

if __name__ == '__main__':

    rtrpass = getpass('enter rtr password: ')

    ssh = connect('10.0.224.25','admin',rtrpass)
    output_data = show_ip_route(ssh)
    pprint(output_data)

    print ('-----------remove \ r and \ n -------------')
    new_strings = []

    for string in output_data:
        new_string = string.replace("\r\n", "")
        new_strings.append(new_string)
    pprint(new_strings)

    ssh.close()


import paramiko
from pprint import pprint

#---- Class to hold information about a generic network device --------
class NetworkDevice():

    def __init__(self, name, ip, user, pw):
        self.name = name
        self.ip_address = ip
        self.username = user
        self.password = pw

    def connect(self):
        self.session = None

    def get_interfaces(self):
        self.interfaces = '--- Base Device, does not know how to get interfaces ---'
    
#---- Class to hold information about an IOS-XE network device --------
class NetworkDeviceIOS(NetworkDevice):

    #---- Initialize --------------------------------------------------
    def __init__(self, name, ip, user, pw):
        NetworkDevice.__init__(self, name, ip, user, pw)

    #---- Connect to device -------------------------------------------
    def connect(self):
        print ('--- connecting IOS: ssh '+self.ip_address)
        # Create paramiko session
        self.ssh_client = paramiko.SSHClient()

        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())


        # Make the connection to our host.
        self.ssh_client.connect(hostname=self.ip_address,
                                username=self.username,
                                password=self.password)
    
        #return self.ssh_client

    #---- Get interfaces from device ----------------------------------
    def get_interfaces(self):

        self.stdin, self.stdout, self.stderr = self.ssh_client.exec_command('show interfaces summary')
        self.interfaces = self.stdout.readlines()



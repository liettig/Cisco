
import time
import getpass
import sys
from netmiko import ConnectHandler
from datetime import datetime
import logging

import jinja2
from jinja2 import Environment, FileSystemLoader    # per template
import yaml                                         # per template
import os                                           # per template

import threading

#===================================================================================
#---- Class to hold information about a generic network device --------
class NetworkDevice():

    def __init__(self, user, pw):
        name = 'Cisco'
        self.username = user
        self.password = pw
        logging.info('sshfunctionnetmiko: created NetworkDevice object for IOS device: %s ', name)

    #---- Connect -----------------------------------------------
    def connect(self):
        print ('--- ssh connecting to: '+self.ip_address+' ---')
        print ('--------------------------------------')
        start_msg = '===> {} Connection to: {}'
        logging.info(start_msg.format(datetime.now().time(), self.ip_address))
        ipaddress = self.ip_address
        # Create netmiko session
        # device_type https://docs.saltstack.com/en/latest/ref/modules/all/salt.modules.netmiko_mod.html
        device_params = {
            'device_type': 'cisco_ios',
            'ip': self.ip_address,
            'username': self.username,
            'password': self.password,
        }
        # connessione ssh al device
        self.ssh_client = ConnectHandler(**device_params)
        # mettiamo nel log la risposta del device
        received_msg = '<=== {} Received from:   {}'
        logging.info(received_msg.format(datetime.now().time(), ipaddress))
        
    
    #---- Get interfaces from device ----------------------------------

    def get_interfaces(self):
        # 'show interfaces summary'
        self.interfaces = self.ssh_client.send_command('show interfaces summary')
        # 'show interfaces summary' in log file
        logging.info('show interfaces summary \n %s', self.interfaces)
    
    def multiple_commands(self):
        self.commands = ['do show ip int brie',
                        'do show ver',
                        'do show inventory']
        self.output = self.ssh_client.send_config_set(self.commands)
        self.show = self.ssh_client.send_command('show interfaces summary')

    
    #---- Push config with YAML and JINJA2 ----------------------------------

    def templateConfig(self):
        filedir = os.path.dirname(__file__)
        yaml_file = os.path.join(filedir, 'Amio.yml')
        jinja_template = os.path.join(filedir, 'Amio.j2')

        def confgen(vars):
            # Generate configuration lines with Jinja2
            with open(jinja_template) as f:
                tfile = f.read()
            template = jinja2.Template(tfile)
            cfg_list = template.render(vars).split('\n')
            #print(cfg_list)
            self.ip_address = vars['hostip']
            self.connect()
            self.output = self.ssh_client.send_config_set(cfg_list)
            logging.info('pushing conf \n %s', self.output)
            
        
        # Parse the YAML file
        with open(yaml_file) as f:
            read_yaml = yaml.safe_load(f)  # Converts YAML file to dictionary
            #print ('####### read_yaml ########\n', read_yaml)

        # Take imported YAML dictionary and start multi-threaded configuration
        #  generation
        for hosts, vars in read_yaml.items():
            # Add host to vars dictionary
            host = {'host': hosts}
            vars.update(host)
            #print ('####vars DOPO aggiunta host #####\n',vars)

            # Send vars dictionary to confgen function using multi-threading,
            #  one thread per-host
            threads = threading.Thread(target=confgen, args=(vars,))
            threads.start()
            print('WAIT ...')
            time.sleep(5)

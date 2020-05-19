
import time
import getpass
import sys
from netmiko import ConnectHandler
from datetime import datetime
import logging

import jinja2
from jinja2 import Environment, FileSystemLoader    # used in template
import yaml                                         # used in template
import os                                           # used in template



#===================================================================================
#---- Class to hold information about a generic network device --------
class NetworkDevice():

    def __init__(self, name, ip, user, pw):
        self.name = name
        self.ip_address = ip
        self.username = user
        self.password = pw
        logging.info('devclassNetmiko: created NetworkDevice object for IOS device: %s %s', name, ip)

    #---- Connect -----------------------------------------------
    def connect(self):
        print ('---------------------------------------------------------')
        print ('--- devclassNetmiko ssh connecting to: '+self.ip_address+' ---')
        # Create netmiko session
        # device_type https://docs.saltstack.com/en/latest/ref/modules/all/salt.modules.netmiko_mod.html
        device_params = {
            'device_type': 'cisco_ios',
            'ip': self.ip_address,
            'username': self.username,
            'password': self.password,
        }
        # ssh connection to the device
        self.ssh_client = ConnectHandler(**device_params)
        # we put in log the device answer
        received_msg = '<=== {} Received from:   {}'
        logging.info(received_msg.format(datetime.now().time(), self.ip_address))
        
    
    #---- Get interfaces from device ----------------------------------

    def get_interfaces(self):
        # we issue 'show interfaces summary'
        self.interfaces = self.ssh_client.send_command('show interfaces summary')
        # we put in log file prne.log the output of 'show interfaces summary'
        logging.info('show interfaces summary \n %s', self.interfaces)
    
    def multiple_commands(self):
        self.commands = ['do show ip int brie',
                        'do show ver',
                        'do show inventory']
        self.output = self.ssh_client.send_config_set(self.commands)
        logging.info('Multiple commands \n %s', self.output)
        #self.show = self.ssh_client.send_command('show interfaces summary')

    #---- Configure EIGRP AS ----------------------------------

    def EIGRP_AS(self):
        self.commands = ['int l0',
                        'ip address 172.16.1.1 255.255.255.0',
                        'int l1',
                        'ip address 172.16.2.1 255.255.255.0',
                        'router eigrp 10',
                        'network 172.16.1.0',
                        'network 172.16.2.0',
                        'no network 172.16.255.0 0.0.0.3',
                        'eigrp router-id 2.2.2.2']
        self.output = self.ssh_client.send_config_set(self.commands)
        #self.show = self.ssh_client.send_command('show ip route')

    def EIGRP_AS_BR2(self):
        self.commands = ['int l0',
                        'ip address 172.16.4.1 255.255.255.0',
                        'int l1',
                        'ip address 172.16.5.1 255.255.255.0',
                        'int l2',
                        'ip address 172.16.6.1 255.255.255.0',
                        'router eigrp 10',
                        'network 172.16.4.0 0.0.3.255',
                        'eigrp router-id 3.3.3.3']
        self.output = self.ssh_client.send_config_set(self.commands)
        #self.show = self.ssh_client.send_command('show ip route')

    def templateInt(self):
        # yaml.safe_load trasform the yml file in python format [List of dictionaries]
        yamldir = os.path.dirname(__file__)
        yaml_template = os.path.join(yamldir, 'TemplateInterfaces1.yml')
        with open(yaml_template) as f:
            routers = yaml.safe_load(f)

        for router in routers:
            jinjadir = os.path.dirname(__file__)
            jinja_template = os.path.join(jinjadir, 'TemplateInterfaces1.j2')
            with open(jinja_template) as f:
                tfile = f.read()    # tfile is TemplateInterfaces1.txt all in a single 
                                    # row and each command split by \n 
            template1 = jinja2.Template(tfile)
            # Convert each line into a list element for passing to Netmiko
            cfg_list = template1.render(router).split('\n') # to merge {} with template1
            self.output = self.ssh_client.send_config_set(cfg_list)
            logging.info('pushing conf \n %s', self.output)
    
            # *** tfile
            # *** 'interface Loopback0\n description Gabriele loopback\n ip address 172.16.{{id0}}.1 255.255.255.0\n!\ninterface Loopback1\n description Gabriele loopback\n ip address 172.16.{{id1}}.1 255.255.255.0\n!\ninterface Loopback2\n description Gabriele loopback\n ip address 172.16.{{id2}}.1 255.255.255.0'

            # *** template1 - module - _body_stream
            # *** ['interface Loopback0...s 172.16.', '', '.1 255.255.255.0\n!...s 172.16.', '', '.1 255.255.255.0\n!...s 172.16.', '', '.1 255.255.255.0']
            # *** 0: 'interface Loopback0\n description Gabriele loopback\n ip address 172.16.'
            # *** 1: ''
            # *** 2: '.1 255.255.255.0\n!\ninterface Loopback1\n description Gabriele loopback\n ip address 172.16.'
            # *** 3: ''
            # *** 4: '.1 255.255.255.0\n!\ninterface Loopback2\n description Gabriele loopback\n ip address 172.16.'
            # *** 5: ''
            # *** 6: '.1 255.255.255.0'

            # *** safe_load
            # *** [
            # *** {'id0': 1, 'id1': 2, 'id2': 3, 'name': 'eng-lab-ch-bel-s-001'}, 
            # *** {'id0': 4, 'id1': 5, 'id2': 6, 'name': 'eng-lab-ch-bel-s-002'}
            # *** ]

            # *** routers
            # *** [
            # *** {'id0': 1, 'id1': 2, 'id2': 3, 'name': 'eng-lab-ch-bel-s-001'}, 
            # *** {'id0': 4, 'id1': 5, 'id2': 6, 'name': 'eng-lab-ch-bel-s-002'}
            # *** ]

            # *** router
            # *** {'id0': 1, 'id1': 2, 'id2': 3, 'name': 'eng-lab-ch-bel-s-001'}

            # *** cfg_list['interface Loopback0', ' description Gabrie... loopback', ' ip address 172.16....255.255.0', '!', 'interface Loopback1', ' description Gabrie... loopback', ' ip address 172.16....255.255.0', '!', 'interface Loopback2', ' description Gabrie... loopback', ' ip address 172.16....255.255.0']
            # *** 00: 'interface Loopback0'
            # *** 01: ' description Gabriele loopback'
            # *** 02: ' ip address 172.16.1.1 255.255.255.0'
            # *** 03: '!'
            # *** 04: 'interface Loopback1'
            # *** 05: ' description Gabriele loopback'
            # *** 06: ' ip address 172.16.2.1 255.255.255.0'
            # *** 07: '!'
            # *** 08: 'interface Loopback2'
            # *** 09: ' description Gabriele loopback'
            # *** 10: ' ip address 172.16.3.1 255.255.255.0'


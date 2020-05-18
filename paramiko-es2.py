import paramiko
import getpass
import sys
import time


command = "show ip int brie"
user = input('Username: ')
password = getpass.getpass()
enable_pass = getpass.getpass(prompt='Enter enable password: ')

devices_ip = ['10.0.224.25', '10.0.224.31', '10.0.224.32']

for ip in devices_ip:
    print('Connection to device {}'.format(ip))
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(
        hostname=ip,
        username=user,
        password=password,
        look_for_keys=False,
        allow_agent=False)

    with client.invoke_shell() as ssh:
        ssh.send('enable\n')
        ssh.send(enable_pass + '\n')
        time.sleep(0.5)

        ssh.send('terminal length 0\n')
        time.sleep(1)
        ssh.recv(1000)

        ssh.send(command + '\n')
        time.sleep(2)
        result = ssh.recv(5000).decode('ascii')
        print(result)
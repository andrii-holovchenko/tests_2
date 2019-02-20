#!/usr/bin/python

import paramiko
import threading
import time

com = raw_input("Please specify the command to run: ")

# Hosts to run the commands on
hosts=['vm1', 'vm2']

def run_ssh_command(host, command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host)
        stdin, stdout, stderr = ssh.exec_command(command)
        print "Command output on %s:" % host
        stdout=stdout.readlines()
        for line in stdout:
            print line
        ssh.close()
    except paramiko.AuthenticationException:
        print "[-] Authentication Exception!"      
         
    except paramiko.SSHException:
        print "[-] SSH Exception!" 

try:
    count=0
    while count < len(hosts):
            threading.Thread(target=run_ssh_command,args=(str(hosts[count]),com)).start()
            time.sleep(0.5)
            count+=1
except Exception, e:
        print '[-] General Exception'



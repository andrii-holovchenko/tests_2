#!/usr/bin/python

import paramiko
import multiprocessing
import time
import argparse
import socket

parser = argparse.ArgumentParser(description='Running ssh commands on multiple hosts')
parser.add_argument("command", type=str, help='Command to run')
parser.add_argument('-l','--list', nargs='+', help='<Required> Space separated hosts', required=True)

def run_ssh_command(host, command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host)
        stdin, stdout, stderr = ssh.exec_command(command)
        print "\nCommand output on [%s]: " % host
        stdout = stdout.read().splitlines()
        stderr = stderr.read()
        if stderr:
            print "[-] Problem occurred while running command: " + command + " The error is " + stderr
        else:
            print "[+] Command execution completed successfully:", command
            for line in stdout:
                print('['+ host + ']:' + line)
        ssh.close()
    except paramiko.AuthenticationException:
        print "[-] Authentication Exception!"
    except paramiko.SSHException as sshException:
        print "[-] SSH Exception!: %s" % sshException
    except socket.timeout as e:
        print "[-] Connection timed out"
    except Exception,e:
        print "[-] Exception in connecting to the server!", host
        print e

if __name__ == '__main__':
    args = parser.parse_args()

    # Command to run
    com = args.command

    # Hosts to run the commands on
    hosts = args.list

    try:
        p = multiprocessing.Pool(4)
        [p.apply(run_ssh_command, args=(hosts[x],com,)) for x in range(len(hosts))]
    except Exception, e:
        print '[-] General Exception:', e



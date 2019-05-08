#!/usr/bin/env python
import time

import paramiko

def monitor_server(socket):
    while(True):
        stdin, stdout, stderr = socket.exec_command('ssh-agent')
        print(stdout.read())
        stdin, stdout, stderr = socket.exec_command('ps -ef | grep -w "sshd:"')
        print(stdout.read())
        stdin, stdout, stderr = socket.exec_command('ss | grep ssh')
        print(stdout.read())
        stdin, stdout, stderr = socket.exec_command('who | wc -l') #Numero de usuarios conectados por ssh
        print(int(stdout.read()))
        stdin, stdout, stderr = socket.exec_command('pinky')
        print(stdout.read())
        time.sleep(5)

def make_connection(hostname, username, password, port):
    socket = paramiko.SSHClient()
    socket.load_system_host_keys()
    socket.connect(hostname, port, username, password)
    monitor_server(socket)
    socket.close()

def main():
    paramiko.util.log_to_file('paramiko.log')
    hostname = ''
    port = 22
    username = ''
    password = ''
    make_connection(hostname, username, password, port)

if __name__ == "__main__":
    main()
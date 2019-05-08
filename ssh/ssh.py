#!/usr/bin/env python
import time

import paramiko

def monitor_server(socket):
	stdin, stdout, stderr = socket.exec_command('ssh-agent')
	agent_info = stdout.read()
	stdin, stdout, stderr = socket.exec_command('ps -ef | grep -w "sshd:"')
	connections_info = stdout.read()
	stdin, stdout, stderr = socket.exec_command('ss | grep ssh')
	socket_info = stdout.read()
	stdin, stdout, stderr = socket.exec_command('who | wc -l') #Numero de usuarios conectados por ssh
	connections = int(stdout.read())
	stdin, stdout, stderr = socket.exec_command('pinky')
	login_info = stdout.read()
	print (" \\begin{itemize}" +
           " \\item status: " + "OK" +
           " \\item interpretacion: " + "Servidor Encendido" +
           " \\item Connections: " + str(connections) +
           " \\item Agent Information: " + str(agent_info) +
           " \\item Connections Informations: " + str(connections_info) +
		   " \\item Socket Informations: " + str(socket_info) +
		   " \\item Socket Informations: " + str(login_info) +
           " \\end{itemize}")

def make_connection(hostname, username, password, port):
	try:
		socket = paramiko.SSHClient()
		socket.load_system_host_keys()
		socket.connect(hostname, port, username, password)
		monitor_server(socket)
		socket.close()
	except Exception as e:
		print (" \\begin{itemize}" +
			   " \\item status: " + "RIP" +
			   " \\item interpretacion: " + "Servidor No response" +
			   " \\item Connections: " + " " +
			   " \\item Agent Information: " + " " +
			   " \\item Connections Informations: " + " " +
			   " \\item Socket Informations: " + " " +
			   " \\item Exception: " + str(e) +
			   " \\end{itemize}")

def main():
    paramiko.util.log_to_file('paramiko.log')
    hostname = ''
    port = 22
    username = ''
    password = ''
    make_connection(hostname, username, password, port)


main()
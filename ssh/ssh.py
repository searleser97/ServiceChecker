#!/usr/bin/env python
import time
import threading

import paramiko

general_status = None
general_message = None

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
           " \\item Agent Information: " + str(agent_info).replace('_', '\_') +
           " \\item Connections Informations: " + str(connections_info) +
		   " \\item Socket Informations: " + str(socket_info) +
		   " \\item Login Information: " + str(login_info) +
           " \\end{itemize}")

def make_connection(hostname, username, password, port):
	global general_status, general_message
	try:
		socket = paramiko.SSHClient()
		socket.load_system_host_keys()
		socket.connect(hostname, port, username, password)
		monitor_server(socket)
		socket.close()
		general_status = "OK"
		general_message = "Servidor Encendido"
	except Exception as e:
		general_status = "RIP"
		general_message = "Servidor No responde"
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
    hostname = '127.0.0.1'
    port = 22
    username = 'Callmetorre'
    password = 'tenisdemesa1'
    make_connection(hostname, username, password, port)

def get_status_ssh_server_multiple_requests(ip):
    start = time.time()
    threads = [threading.Thread(target=main) for _ in range(10)]
    [t.start() for t in threads]
    [t.join() for t in threads]
	response = round(time.time() - start, 2)
    print (" \\begin{itemize}" +
		   " \\item status: " + str(general_status) +
		   " \\item numero de peticiones " + str(20) +
           " \\item time response of 20 clients " + str(response) + " s"
           " \\end{itemize}")

if __name__ == "__main__":
    main()
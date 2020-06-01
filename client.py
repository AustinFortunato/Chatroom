#!/usr/bin/env python3

import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = f"192.168.1.{sys.argv[1]}"
port = 42069
buff = 10

types = {
	0 : "Register",
	1 : "Login",
	2 : "Send Global",
	3 : "Send To",
	4 : "Log Off",
	5 : "Server Message"
}


# Sends a message
def send(message, message_type):
	message_length = len(message)
	header = message_length + " "*(buff-len(str(message_length))) + str(message_type)
	s.send((header + message).encode('utf-8'))


# Receives message and breaks it into peices
def receive():
	message_size = int(conn.recv(buff).decode('utf-8'))
	message = ''

	while len(message) < message_size:
		if message - len(message_size) < chunk:
			message += s.recv(message - len(message_size)).decode('utf-8')
		else:
			message += s.recv(chunk).decode('utf-8')

	message_type = int(message[:1])
	return message_type
	return message[1:]


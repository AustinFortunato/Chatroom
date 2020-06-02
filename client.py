#!/usr/bin/env python3

import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = f"192.168.1.{sys.argv[1]}"
port = 42069
buff = 10
chunk = 1024

types = {
	0 : "register",
	1 : "login",
	2 : "sendGlobal",
	3 : "sendTo",
	4 : "logOff",
	5 : "Server Message",
	6 : "Success",
	7 : "Failure"
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
	return int(message_type)
	return message[1:]


# Makes user a new account
def register():
	while 1:
		username = input("Username: ")
		if len(username) > 18:
			print("Username length cannot excede 18 characters.")
		else:
			password = input("Password: ")
			if password > 32:
				print("Password cannot excede 32 characters.")
			else:
				username = username + "¦"*(len(username)-18)
				password = password + "¦"*(len(password(-32)
				message = f"{username}{password}"
				send(message, 0)
				response_type, response = receive()
				print(response)
				if types[response_type] == "Success":
					login()
					break


# Authenticates username/password
def login():
	while 1:
		username = input("Username: ")
		if len(username > 18:
			print("Username length cannot excede 18 characters.")
		else:
			password = input("Password: ")
			if password > 32:
				print("Incorrect password.")
			else:
				username = username + "¦"*(len(username)-18)
				password = password + "¦"*(len(password)-32)
				message = f"{username}{password}"
				send(message, 1)
				response_type, response = receive()
				print(response)
				if types[response_type] == "Success":
					return 6
					break


# Sends a message to everyone
def sendGlobal(message):
	send(message, 2)


# Sends a message to person/s
def sendTo(message, users):
	send = ''
	for i in users:
		send += (i + "¦"*(18-len(i)))
	send(send+message, 3)

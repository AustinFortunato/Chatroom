#!/usr/bin/env python3

import socket
import sys

parameter = sys.argv[1]
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_STREAM, socket.SO_REUSEADDR, 1)

host = ""
port = 42069
buff = 10
chunk = 1024

users = {}
connections = {}
loggedIn = []
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
def send(conn, message, message_type):
	message_length = len(message)
	header = str(message_length+1) + " "*(buff-len(str(message_length))+1) + str(message_type)
	conn.send((header + message).encode('utf-8'))


# Receives message and breaks it into peices
def receive(conn):
	message_size = int(conn.recv(buff).decode('utf-8'))
	message = ''

	while len(message) < message_size:
		if message - len(message_size) < chunk:
			message += conn.recv(message - len(message_size)).decode('utf-8')
		else:
			message += conn.recv(chunk).decode('utf-8')

	message_type = int(message[:1])
	return message_type
	return message[1:]


# Registers a new user
def register(conn, message):
	username = message[:18].split("¦")
	password = message[18:50].split("¦")
	if username not in users:
		send(conn, f'Registered, {username}', 6)
		users[username] = password
		connections[conn] = username
	else:
		send(conn, 'Username already taken!', 7)


# Authenticates a users login
def login(conn, message):
	username = message[:18].split("¦")
	password = message[18:50].split("¦")
	if username in users:
		if users[username] == password:
			send(conn, f'Logged in {username}', 6)
			loggedIn.append(users[username])
		else:
			send(conn, 'Incorrect Username/Password', 7)
	else:
		send(conn, 'Incorrect Username/Password', 7)


# Sends a message to everyone
def sendGlobal(conn, message):
	user = connections[conn]
	for i in connections:
		if i != conn and i in loggedIn:
			send(i, f'{user} > {message}', 2)


# Sends to user/s
def sendTo(conn, message):
	num_recipients = int(message[:2])
	recipients = []
	for i in num_recipients:
		recipients.append(message[(i-1)*18:i*18].split("¦"))
	for i in recipients:
		if i in loggedIn:
			send(list(users.keys())[list(users.values()).index(i)], f'{users[conn]} > {message[2+recipients*18:]}', 3)


# Logs a user off
def logOff(conn):
	loggedIn.pop(users[conn])


# Runs the server and logic.
s.bind((host,port))
while True:
	conn, addr = s.accept()
	connections[conn] = addr
	if conn:
		send(conn, "Connected...", 5)
		message_type, message = receive(conn)
		if message_type == 4:
			logOff(conn)
			conn.close()
		elif message_type in types:
			exec(f"{types[message_type]}(conn, message)")

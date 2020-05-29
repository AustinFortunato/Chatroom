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
	0 : "Register"
	1 : "Login"
	2 : "Send Global"
	3 : "Send To"
	4 : "Log Off"
}


# Sends a message
def send(conn, message):
	pass


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
		send(conn, f'Registered, {username}')
		users[username] = password
		connections[conn] = username
	else:
		send(conn, 'Username already taken!')


# Authenticates a users login
def login(conn, message):
	username = message[:18].split("¦")
	password = message[18:50].split("¦")
	if username in users:
		if users[username] == password:
			send(conn, f'Logged in {username}')
			loggedIn.append(users[username])
		else:
			send(conn, 'Incorrect Username/Password')
	else:
		send(conn, 'Incorrect Username/Password')


# Sends a message to everyone
def sendGlobal(conn, message):
	user = connections[conn]
	for i in connections:
		if i != conn && i in loggedIn:
			send(i, (f'2{user} > {message}').encode('utf-8'))


# Sends to user/s
def sendTo(conn, message):
	num_recipients = int(message[:2])
	recipients = []
	for i in num_recipients:
		recipients.append(message[(i-1)*18:i*18].split("¦"))
	for i in recipients:
		if i in loggedIn:
			send(list(users.keys())[list(users.values()).index(i)], f'3{users[conn]} > {message[2+recipients*18:]}')


# Logs a user off
def logOff(conn):
	loggedIn.pop(users[conn])

# Testing Script 

import socket                                                # Import socket module
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object
s.bind(('192.168.4.1', 1234))                                 # basically (IP, Port)
s.listen(5)                                                   # que of 5

while True:
    clientsocket, address = s.accept()                        # Wait for msg
    
    print(f"Connection from {address} has been established!")
    clientsocket.send(bytes("Welcome to the server!", "utf-8")) # Send connection confirmation

    msg = clientsocket.recv(2048)                              # Get data
    msg = json.loads(msg.decode())                             # Reformat into json obj
    array = msg.get("array")                                   # Extract array
    for i in (array):                                          # Print array
        print(i)

    clientsocket.send(bytes("GTG", "utf-8"))                   # Send GTG if msg is good / ERROR if it is bad

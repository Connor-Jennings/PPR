import socket               # Import socket module

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object
s.connect(('192.168.4.1', 1234))

msg  = s.recv(1024)
print(msg.decode("utf-8"))

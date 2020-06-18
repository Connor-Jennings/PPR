# Connor Jennings
# June/2020
# TestServer.py
# This script is just for testing the client script

#########################################################################################################
# KEY TERMS:
IP = '192.168.4.1'
PORT = 1234

#########################################################################################################
#                                           Objects                                                     #
#########################################################################################################
# Libraries
import socket                                                # Import socket module
import json

#########################################################################################################


def Transmit(formatted_data):
    if(raw_data == 0):
        return False
    return True

def Check_data(raw_data):
    if(raw_data[0] == -1):
        return -1
    i = len(raw_data)
    if (i == 0):
        return "ERROR"

#########################################################################################################
#                                            Main                                                       #
#########################################################################################################

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)             # Create a socket object
    s.bind((IP, PORT))                                                # basically (IP, Port)
    s.listen(5)                                                       # que of 5

    while True:
        clientsocket, address = s.accept()                            # Wait for msg

        print(f"Connection from {address} has been established!")
        clientsocket.send(bytes("Welcome to the server!", "utf-8"))   # Send connection confirmation

        msg = clientsocket.recv(4096)                                 # Get data
        msg = json.loads(msg.decode())                                # Reformat into json obj
        array = msg.get("array")                                      # Extract array
        for i in (array):                                             # Print array
            print(i)

        response = Check_data(array)                                  # Check if Data in array is valid
        if (response == -1):                                          # If client sends -1 close socket
            break

        if(Transmit(array)):                                          # Attempt transmission and send response to client
            clientsocket.send(bytes(response, "utf-8"))                   
        else:
            clientsocket.send(bytes("MsgNotSent", "utf-8"))



if __name__ == "__main__":
    print("-----------------Server Has Started--------------------------")
    main()
    print("Connection Closed")

# Connor Jennings
# June/2020
# Server.py

#########################################################################################################
# KEY TERMS:
IP = '192.168.4.1'
PORT = 1234
# Libraries
import socket
import json          

#########################################################################################################
#                                           Functions                                                   #
#########################################################################################################

def Transmit(formatted_data):                                         # Send the data to the Trasmitter
    if(formatted_data == 0):
        return False
    return True

def Check_data(raw_data):                                             # Check the data from the client for errors
    if(raw_data[0] == "-1"):                                          # Look for "-1" to end the server program
        return "-1"
    i = len(raw_data)
    if (i !=3 and i != 4):                                            # If the data is not the right size return Error 
        return "ERROR"
    return "GTG"

def Format(array):                                                    # Put the data into a radio ready format
    return "whateverformatthetransmitterwillrequire"

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
        array = msg.get("array")                                      # Extract data
        for i in (array):                                             # Print data
            print("\t\t"+i)

        response = Check_data(array)                                  # Check if Data in data is valid
        if (response == "-1"):                                        # If client sends -1 close socket
            clientsocket.send(bytes("FINAL", "utf-8"))
            s.shutdown(socket.SHUT_RDWR)
            s.close()
            return

        formatted_data = Format(array)

        if(Transmit(1)):                                              # Attempt transmission and send respond to client
            clientsocket.send(bytes(response, "utf-8"))                   
        else:
            clientsocket.send(bytes("MsgNotSent", "utf-8"))
    

if __name__ == "__main__":
    print("-----------------Server Has Started--------------------------")
    main()
    print("Connection Closed")

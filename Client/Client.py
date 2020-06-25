# Connor Jennings 
# June/2020
# ClientBuilder.py

#########################################################################################################
# KEY TERMS: 
#   In BuildConnection.FeedbackHandler [ GTG = Everyting is Good to Go, 
#                                       Error = An Error Occurred )
#   In Communication.Talk ( ONCE = send one time[default], 
#                           TRACK = send at intervals unitl stopped,
#                           TXT = written message appended to end of normal message, 
#                           END = tell server to close socket)  -->MODE
IP = "192.168.4.1"
PORT = 1234
MODE = "ONCE"
DELAY = 300                                                         # 300 second delay for TRACK mode (5min)
# Libraries
import socket                                                        # Import socket module
import location                                                      # This import is iOS specific
import time                                                          # For sleep() in Communication obj
import array                                                         # Data container
import json                                                          # For sending data

#########################################################################################################
#                                           Objects                                                     #
#########################################################################################################

# Establish a connection between client and server, then prints message from the server
class BuildConnection:                                                        
    def __init__(self, ipaddress='', port=0,  message="", hostfeedback="", s=0): # Initalize variables
        self.ipaddress = ipaddress        
        self.port = port 
        self.message = message
        self.hostfeedback = hostfeedback
        self.s = s               

    def SetIP(self, ipa):                                             # Set a new IP Address
        self.ipaddress = ipa

    def SetPort(self, new_port):                                      # Set a new port
        self.port = new_port
    
    def Connect(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # Create a socket object
        self.s.connect((self.ipaddress, self.port))                   # Connnect to new host

        msg = self.s.recv(4096)                                       # Get message that host should send
        msg = msg.decode("utf-8")
        print(msg)                                                    # Print that message
    
    def Feedbackhandler(self):                                        # Handle feedback from host
        if (self.hostfeedback == "GTG"):                              
            print(" ->Message Is Good")
        elif (self.hostfeedback == "FINAL"):
            print(" ->Server Port Closed")  
        elif (self.hostfeedback == "ERROR"):                          
            print(" ->MESSAGE FAILED \n\t ->Format Error")
        elif (self.hostfeedback == "MsgNotSent"):
            print(" ->MESSAGE FAILED \n\t ->Transmission Error")
        elif (self.hostfeedback == ""): 
            print(" ->No Feedback From Server")
        else:
            print(" ->Feedaback From Server Not Recognized")

    def Submit(self):                                                  
        data = json.dumps({"array": self.message})                    
        self.s.send(data.encode())                                # Send message to Host                   
        print("-->Message Sent ")
        for i in (self.message):
            print(("\t\t" + str(i))) 

        feedback = self.s.recv(4096)                              # Get Feedback
        self.hostfeedback = feedback.decode("utf-8")
        self.Feedbackhandler()

    def Close(self):
        self.s.shutdown(socket.SHUT_RDWR)
        self.s.close()
        print(" ->Client Port Closed")


#########################################################################################################
# Build a message to send to the host, it consists of coordinates and a timestamp 
class BuildMessage:
    def __init__(self, txt= "", lat="", lng="", timestamp=""):
        self.txt = txt                  
        self.lat = lat
        self.lng = lng
        self.timestamp = timestamp

    def SetVariables(self):                                            # Get current location and time
        location.start_updates()                                       # Get location data from Phone
        loc = location.get_location()
        location.stop_updates()

        if (self.lat == ""):                                           # Set the Data if it's not already set
            self.lat = str(loc['latitude'])
        if (self.lng == ""):
            self.lng = str(loc['longitude'])
        if (self.timestamp == ""):
            self.timestamp = str(loc['timestamp'])
        
    def Build(self):                                                   # Build  the message 
        self.SetVariables()                                            # Fetch Data

        message = [self.lat]                                           # Format Data
        message.append(self.lng)
        message.append(self.timestamp)
        if(self.txt != ""):
            message.append(self.txt)

        return message                                                 # Return


#########################################################################################################
# Goes through all of the steps to complete a communication with the Host
class Communication:
    def __init__(self, ip="", port="", delay=""):
        self.ip = ip
        self.port = port
        self.delay = delay

    def Word(self, txt=""):
        if(txt == "-1"):
            message = [txt]
            connect = BuildConnection(self.ip, self.port, message)    # Create connection obj for END mode
        else:
            messageobj = BuildMessage(txt)                                    # Build a message to send
            connect = BuildConnection(self.ip, self.port, messageobj.Build()) # Create default connection obj  

        connect.Connect()                                              # Establish Connection  
        connect.Submit()                                               # Send the message and deal with errors
        connect.Close()                                                # Close the socket
        
        del connect                                                    # Delete obj to refresh data

    def Talk(self, mode=""):
        if(mode == "ONCE" or mode == ""):                                       # Sends message then closes session
            self.Word()
        elif(mode == "TRACK"):
            while (True):                                              # TRACK Continues unitl interuppted 
                self.Word()
                time.sleep(self.delay)                                 # Wait to send again
        elif(mode == "TXT"):
            txt = input("Enter Message: ")
            self.Word(txt)
        elif(mode == "END"):
            self.Word("-1")
        else:
            print("Mode Not Recognized")
        

#########################################################################################################
#                                           MAIN                                                        #
#########################################################################################################

def main():
    GPS = Communication(IP, PORT, DELAY)                               # Initialize the builder 
    GPS.Talk(MODE)                                                     # Start the communication                        


if __name__ == "__main__":
    print("-------------------------------------------")
    main()
    print("")

# Connor Jennings 
# June/2020
#########################################################################################################
# KEY TERMS: 
#   FeedbackHandler( GTG = Everyting is Good to Go, Error = An Error Occurred )
#   Communication.Talk(ONCE = send one time[default], TRACK = send at intervals unitl stopped
#       TXT = written message appended to end of normal message) -->MODE
IP = "192.168.4.1"
PORT = 1234
MODE = "ONCE"
DELAY = 300                                                         # 300 second delay for TRACK mode (5min)
#########################################################################################################
#                                           Objects                                                     #
#########################################################################################################
# Libraries
import socket                                                        # Import socket module
import location                                                      # This import is iOS specific
import time                                                          # For sleep() in Communication obj


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

        msg  = self.s.recv(1024)                                      # Get message that host should send
        print(msg.decode("utf-8"))                                    # Print that message
    
    def Feedbackhandler(self):                                        # Handle feedback from host
        if (self.hostfeedback == "GTG"):                              # Successful Transmission
            print("-->Message is Good")  
            return
        if (self.hostfeedback == "ERROR"):                            # Error Handler
            print("-->MESSAGE FAILED \n\t-->[Error Description]")

    def Submit(self):                                                  
        while(self.hostfeedback == ""):                         
            self.s.send(bytes(self.message, "utf-8"))                 # Send message to Host                   
            print("-->Message Sent" + " ( " + self.message+ " ) ")  

            self.hostfeedback ="1"
            feedback = self.s.recv(1024)                              # Get Feedback
            self.hostfeedback = feedback.decode("utf-8")
            self.Feedbackhandler()

    def Close(self):
        self.s.close()
        print("-->Connection Closed")


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

        message = self.lat + " "                                       # Format Data
        message += self.lng + " "
        message += self.timestamp
        if(self.txt != ""):
            message += " " + self.txt

        return message                                                 # Return


#########################################################################################################
# Goes through all of the steps to complete a communication with the Host
class Communication:
    def __init__(self, ip="", port="", mode="", delay=""):
        self.ip = ip
        self.port = port
        self.mode = mode
        self.delay = delay

    def Word(self, txt=""):
        messageobj = BuildMessage(txt)                                    # Build a message to send

        connect = BuildConnection(self.ip, self.port, messageobj.Build()) # Establish Connection  
        connect.Connect()
                                       
        connect.Submit()                                               # Send the message and deal with errors
        connect.Close()                                                # Close the socket
        
        del connect                                                    # Delete obj to start fresh if "TRACK" is on

    def Talk(self):
        if(self.mode == "ONCE"):                                       # Sends message then closes session
            self.Word()
        elif(self.mode == "TRACK"):
            while (True):                                              # TRACK Continues unitl interuppted 
                self.Word()
                time.sleep(self.delay)                                 # Wait to send again
        elif(self.mode == "TXT"):
            txt = input("Enter Message: ")
            self.Word(txt)
        

#########################################################################################################
#                                           MAIN                                                        #
#########################################################################################################

def main():
    GPS = Communication(IP, PORT, MODE, DELAY)                         # Initialize the builder 
    GPS.Talk()                                                         # Start the communication                        


if __name__ == "__main__":
    print("-------------------------------------------")
    main()
    print("")

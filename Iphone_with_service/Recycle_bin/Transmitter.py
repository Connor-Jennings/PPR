# Connor Jennings 
# June/2020
# Transmitter.py

#########################################################################################################
# Key Terms: 
#                     MODE ( ONCE = send one time[default], 
#                            TRACK = send at intervals unitl stopped,
#                            TXT = written message appended to end of normal message )
#
#                    TRIP_ID = [name of the trip to be matched with in server]
#
#                    DELAY = [ammount of time to delay when the track mode is set] 
MODE = "ONCE"                                                        # Action program should perform
TRIP_ID = "Default"                                                   
DELAY = 300                                                          # 300 second delay for TRACK mode (5min)

# Libraries
import requests 
import re
import selenium                                                      # Use selenium to navigate to the webpage
import location                                                      # This import is iOS specific
import time                                                          # For sleep() in Communication obj
import array                                                         # Data container
import json                                                          # For sending data
#########################################################################################################
#                                           Objects                                                     #
#########################################################################################################
# Build a message to send to the host, it consists of coordinates and a timestamp 
class BuildMessage:
    def __init__(self, trip_id="", txt= "", lat="", lng="", timestamp=""):
        self.trip_id = trip_id
        self.txt = txt                  
        self.lat = lat
        self.lng = lng
        self.timestamp = timestamp

    def SetVariables(self):                                          # Get current location and time
        location.start_updates()                                     # Get location data from Phone
        loc = location.get_location()
        location.stop_updates()

        if (self.trip_id == ""):
            self.trip_id = "NO_NAME"
        if (self.lat == ""):                                         # Set the Data if it's not already set
            self.lat = str(loc['latitude'])
        if (self.lng == ""):
            self.lng = str(loc['longitude'])
        if (self.timestamp == ""):
            self.timestamp = str(loc['timestamp'])
        
    def Build(self):                                                 # Build  the message 
        self.SetVariables()                                          # Fetch Data

        message = [self.trip_id]                                     # Format Data
        message.append(self.lat)
        message.append(self.lng)
        message.append(self.timestamp)
        message.append(self.txt)

        return message                                              # Return

# Handle building a message to send and send it 
class Transmit:
    def __init__(self, mode="", delay=""):
        self.mode = mode
        self.delay = delay

    def Word(self, txt=""):
        messageobj = BuildMessage(TRIP_ID, txt)                    # Build a message to send  
        message = messageobj.Build()

        ##########################
        # Send Message to Server #
        ##########################
        driver = webdriver.Chrome()                                 # Use chrome as my browser
        driver.get('https://MolokiToOahuVirtualRace/addData.html')  # Open the website
        
        id_box = driver.find_element_by_name('title')               # Select the boxes an input info
        id_box.send_keys(message[0])

        id_box = driver.find_element_by_name('lat') 
        id_box.send_keys(message[1])
        
        id_box = driver.find_element_by_name('lng') 
        id_box.send_keys(message[2])
        
        id_box = driver.find_element_by_name('timeStamp') 
        id_box.send_keys(message[3])

        id_box = driver.find_element_by_name('txt') 
        id_box.send_keys(message[4])
        
        id_box = driver.find_element_by_name('status') 
        id_box.send_keys('')

        submit_button = driver.find_element_by_value('status') 
        submit_button.click()

    def Talk(self):
        if(self.mode == "ONCE" or self.mode == ""):                 # Sends message then closes session
            self.Word()
        elif(self.mode == "TRACK"):
            while (True):                                           # TRACK Continues unitl interuppted 
                self.Word()
                time.sleep(self.delay)                              # Wait to send again
        elif(self.mode == "TXT"):
            txt = input("Enter Message: ")
            self.Word(txt)
        else:
            print("Mode Not Recognized")
        


#########################################################################################################
#                                           MAIN                                                        #
#########################################################################################################

def main():
    GPS = Transmit(MODE, DELAY)                                     # Initialize the builder 
    GPS.Talk()                                                      # Start the communication                        


if __name__ == "__main__":
    print("-------------------------------------------")
    main()
    print("")

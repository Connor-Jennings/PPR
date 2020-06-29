# Connor Jennings 
# June/2020
# WithService.py

#########################################################################################################
# KEY TERMS: 
#   In BuildConnection.FeedbackHandler [ GTG = Everyting is Good to Go, 
#                                       Error = An Error Occurred )
#   In Communication.Talk ( ONCE = send one time[default], 
#                           TRACK = send at intervals unitl stopped,
#                           TXT = written message appended to end of normal message, 
#                           END = tell server to close socket)  -->MODE
MODE = "TRACK"
DELAY = 300                                     # 300 second delay for TRACK mode (5min)
TRIP_ID = "Default" 
URL = 'http://192.168.86.199:80/addData.html'

# Libraries                              
import location                                                      
import time                                                          
import array                                                                                                                
import requests

#########################################################################################################
#                                        FUCNCTIONS                                                     #
#########################################################################################################
def Output(trip_id="", lat="", lng="", timestamp="", txt=""):
    print('trip id     : '+trip_id)
    print('lat         : '+lat)
    print('lng         : '+lng)
    print('time        : '+timestamp)
    if (txt != ""):
        print('text        : '+txt)

def Submit_data(trip_id="", lat="", lng="", timestamp="", txt=""):
    # Reach out to the website
    response = requests.get(URL)

    if(response.status_code == 200):
        print('Request was successful')
        parameters = {'title':trip_id,'lat':lat,'lng':lng,'timeStamp':timestamp,'txt':txt}
        requests.post(URL, data = parameters)
    elif(response.status_code == 404):
        print('Site not found')
    else:
        print('Some error occured')

        print("Data Submitted")


#########################################################################################################
#                                           MAIN                                                        #
#########################################################################################################
def main():
# TRACKING MODE 
    if (MODE == "TRACK"):
        location.start_updates()                                      
        loc = location.get_location()
        location.stop_updates()
        time_of_last_submission = loc['timestamp']
        
        first_loop = True
        while(True):
            # The location needs to be reset each time because of data being cashed 
            location.start_updates()                                     # Retreive Data
            loc = location.get_location()
            location.stop_updates()

            lat = str(loc['latitude'])                                   # Parse Data
            lng = str(loc['longitude'])
            timestamp = str(loc['timestamp'])
            now = loc['timestamp']
            time_passed = int(now - time_of_last_submission)

            Output(TRIP_ID,lat,lng,timestamp)                                    # Output Data
            print('time passed : '+ str(time_passed))
           
            # only submit data on first loop and when the DELAY time has been reached
            if(time_passed >= DELAY or first_loop):
                Submit_data(TRIP_ID,lat,lng,timestamp)
                time_of_last_submission = now
                first_loop = False
            print()

            # sleep for 5 seconds then fetch new data
            time.sleep(5)                                 

    # tracking mode has cashing issues when its not isolated
    else:
        location.start_updates()                                        # Retreive Data
        loc = location.get_location()
        location.stop_updates()

# ONCE MODE / DEFAULT
        if(MODE == "ONCE" or MODE == ""):                
            location.start_updates()                                     # Retreive Data
            loc = location.get_location()
            location.stop_updates()

            lat = str(loc['latitude'])                                   # Parse Data
            lng = str(loc['longitude'])
            timestamp = str(loc['timestamp'])

            Output(TRIP_ID,lat,lng,timestamp)                                    # Output Data
            Submit_data(TRIP_ID,lat,lng,timestamp)

# TEXT MODE
        elif(MODE == "TXT"):
            txt = input("Enter Message: ")

            location.start_updates()                                     # Retreive Data
            loc = location.get_location()
            location.stop_updates()

            lat = str(loc['latitude'])                                   # Parse Data
            lng = str(loc['longitude'])
            timestamp = str(loc['timestamp'])

            Output(TRIP_ID,lat,lng,timestamp,txt)                                    # Output Data
            Submit_data(TRIP_ID,lat,lng,timestamp,txt)

# ERROR CATCHER
        else:
            print("Mode Not Recognized")


#########################################################################################################        
if __name__ == "__main__":
    print("-------------------------------------------")
    main()
    print("")

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


# Libraries                              
import location                                                      
import time                                                          
import array                                                                                                                
import mechanize

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
    br = mechanize.Browser()
    br.set_handle_equiv(False)
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    br.open('https://www.project-found.com/addData.html')
    
    response = br.response()
    
    br.select_form('myform')
    
    br.form['title'] = trip_id
    br.form['lat'] = lat
    br.form['lng'] = lng
    br.form['timeStamp'] = timestamp
    br.form['txt'] = txt
    
    br.submit()
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
            avglat =0
            avglng =0
            avgtime =0
            it =0
            # work around for apples location accuracy restrictions
            while(it<50):
                location.start_updates()                                     # Retreive Data
                loc = location.get_location()
                location.stop_updates()
                avglat += loc['latitude']
                avglng += loc['longitude']
                avgtime += loc['timestamp']
                it += 1

            

            lat = str(avglat/50)                                   # Parse Data
            lng = str(avglng/50)
            timestamp = str(avgtime/50)
            now = avgtime/50
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
            time.sleep(10)                                 

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

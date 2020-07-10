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
DELAY = 150                                     # 300 second delay for TRACK mode (5min)
TRIP_ID = "Default" 
 

# Libraries                              
import location                                                      
import time                                                          
import array                                                                                                                
import mechanize
from objc_util import ObjCInstance, ObjCClass, ObjCBlock, c_void_p

#########################################################################################################
#                                        FUCNCTIONS                                                     #
#########################################################################################################
def Output(trip_id="", lat="", lng="", timestamp="", bp="", txt=""):
    print('trip id     : '+trip_id)
    print('lat         : '+lat)
    print('lng         : '+lng)
    print('time        : '+timestamp)
    print('Air Pressure: '+bp)
    if (txt != ""):
        print('text        : '+txt)
 
def Submit_data(trip_id="", lat="", lng="", timestamp="", txt="", bp=""):
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
    br.form['BP'] = bp
    
    br.submit()
    print("Data Submitted", end=" ")
    print(get_pressure())

pressure = None

def get_pressure():

  def handler(_cmd, _data, _error):
    global pressure
    pressure = ObjCInstance(_data).pressure()

  handler_block = ObjCBlock(handler, restype=None, argtypes=[c_void_p, c_void_p, c_void_p])

  CMAltimeter = ObjCClass('CMAltimeter')
  NSOperationQueue = ObjCClass('NSOperationQueue')
  if not CMAltimeter.isRelativeAltitudeAvailable():
    print('This device has no barometer.')
    return
  altimeter = CMAltimeter.new()
  main_q = NSOperationQueue.mainQueue()
  altimeter.startRelativeAltitudeUpdatesToQueue_withHandler_(main_q, handler_block)
  #print('Started altitude updates.')
  try:
    while pressure is None:
      pass
  finally:
    altimeter.stopRelativeAltitudeUpdates()
    #print('Updates stopped.')
    return pressure

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
        buffer = []
 
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
            bp = str(get_pressure())
 
            current_data = [lat, lng, timestamp, bp]
 
            Output(TRIP_ID,lat,lng,timestamp,bp)                                    # Output Data
            print('time passed : '+ str(time_passed))
           
            # only submit data on first loop and when the DELAY time has been reached
            if(time_passed >= DELAY or first_loop):
                try:
                    if(len(buffer) == 0):
                        Submit_data(TRIP_ID, current_data[0], current_data[1], current_data[2], current_data[3])
                    else:
                        buf_it = len(buffer) 
                        while(buf_it > 0):
                            Submit_data(TRIP_ID, buffer[buf_it-1][0], buffer[buf_it-1][1], buffer[buf_it-1][2], buffer[-1][3])
                            time_of_last_submission = now
                            buffer.pop(buf_it-1)
                            buf_it = buf_it - 1
                        Submit_data(TRIP_ID, current_data[0], current_data[1], current_data[2], current_data[3])
                except:
                    print("Data Not Submitted, Service Error")
                    buffer.append(current_data)
                    
                print("Buffer("+str(len(buffer))+")")
                first_loop = False
            print()
 
            # sleep for 10 seconds then fetch new data
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
            bp = str(get_pressure())
 
            Output(TRIP_ID,lat,lng,bp,timestamp)                                    # Output Data
            Submit_data(TRIP_ID,lat,lng,timestamp,bp)
 
# TEXT MODE
        elif(MODE == "TXT"):
            txt = input("Enter Message: ")
 
            location.start_updates()                                     # Retreive Data
            loc = location.get_location()
            location.stop_updates()
 
            lat = str(loc['latitude'])                                   # Parse Data
            lng = str(loc['longitude'])
            timestamp = str(loc['timestamp'])
            bp = str(get_pressure())
 
            Output(TRIP_ID,lat,lng,timestamp,bp,txt)                                    # Output Data
            Submit_data(TRIP_ID,lat,lng,timestamp,txt,bp)
 
# ERROR CATCHER
        else:
            print("Mode Not Recognized")
 
#########################################################################################################        
if __name__ == "__main__":
    print("-------------------------------------------")
    main()
    print()
  
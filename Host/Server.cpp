// Connor Jennings
// June/2020

#include <iostream>
#include "Server.h"


//                                Builder Function                                         //
void Builder::Construct(){
  std::cout<< "THis shit worked yooooooooooooooo\n";
}


//                                Connect Functions                                       //
void Connect::EstablishConnection(){                            // Establish this device as a server using "ip" and "port"
}
void Connect::Listen(){                                         // Wait for a connection to be made at "port" and deal with the message
}
void Connect::CloseConnection(){                                // Safely close port and exit program
}
std::string Connect::ErrorCheck(std::string[]){                 // Create message to send back to client depending on the data received
}


//                              Transmit Functions                                       //
void Transmit::FormatData(){                                    // Format the data into a usable format for the transmitter
}
void Transmit::Send(){                                          // Send data to Ham Radio
}


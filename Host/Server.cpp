// Connor Jennings
// June/2020

#include "Server.h"
#include <iterator>

//                                Builder Function                                         //
void Builder::Construct(){
  std::cout<< "THis shit worked yooooooooooooooo\n";
}


//                                Connect Functions                                       //
Connect::Connect(std::string set_ip, int set_port, std::vector<std::string> set_message, int set_stream){  // Constructor
  ip = set_ip;
  port = set_port;
  message = set_message;
  stream = set_stream;
}

void Connect::EstablishConnection(){                            // Establish this device as a server using "ip" and "port"
}

void Connect::Listen(){                                         // Wait for a connection to be made at "port" and deal with the message
}

void Connect::CloseConnection(){                                // Safely close port and exit program
}

std::string Connect::ErrorCheck(std::string[]){                 // Create message to send back to client depending on the data received
}


//                              Transmit Functions                                       //
Transmit::Transmit(std::string set_data, int set_frequency){    // Constructor
  data = set_data;
  frequency = set_frequency;
}

void Transmit::FormatData(){                                    // Format the data into a usable format for the transmitter
}

void Transmit::Send(){                                          // Send data to Ham Radio
}

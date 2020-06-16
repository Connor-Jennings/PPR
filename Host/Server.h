// Connor Jennings
// June/2020
// Server.h
//--------------------------------------Includes----------------------------------------------------//
#include <iostream>
#include <string>
#include <vector>


//                                   Class Declarations                                            //

/* Builder --> Compiles everything the server needs to do into one place                          */
class Builder {

  public:
    void Construct();                                     // Uses other classes to carry out the servers duty

};



// Connect --> Acts as a server and deal with client connections
class Connect {

  private:
    std::string ip;
    int port;
    std::vector<std::string> message;
    int stream;                                           // Stream variable to use in functions

  public:
    Connect(std::string, int, std::vector<std::string>, int);           // Constructor

    void EstablishConnection();                           // Establish this device as a server using "ip" and "port"
    void Listen();                                        // Wait for a connection to be made at "port" and deal with the message
    void CloseConnection();                               // Safely close port and exit program
    std::string ErrorCheck(std::string[]);                // Create message to send back to client depending on the data received

};



// Transmit --> Takes message received by "Connect", formats into permissiable digital mode for radio, then passes data onto transmitter
class Transmit {

  private:
    std::string data;
    int frequency;

  public:
    Transmit(std::string, int);

    void FormatData();                                    // Format the data into a usable format for the transmitter
    void Send();                                          // Send data to Ham Radio

};


// Connor Jennings
// June/2020
// Server.cpp

#include "Server.h"

// Macros
#define IP "192.168.4.1"
#define PORT 1234

// String to char array
void StringToCharArray(std::string str, char* c){ //Takes string to be converted then pointer to char array to be filled
  str.copy(c, str.size() + 1);
  // c[str.size()] = '\0';
}


//                                Builder Function                                         //
void Builder::Construct(){                                       // Use other classes to carry out the servers duty
  std::cout<< "---------Server Started---------" << std::endl;
  Connect GPS(IP, PORT, 0);
  int code = GPS.EstablishConnection();
  if (code == 0){
    GPS.Listen();
    GPS.CloseConnection();
  }
}


//                                Connect Functions                                       //
Connect::Connect(const char* set_ip, int set_port, int set_clientSocket){  // Constructor
  ip = set_ip;
  port = set_port;
  clientSocket = set_clientSocket;
}

int Connect::EstablishConnection(){                            // Establish this device as a server using "ip" and "port"
  // Create a socket
  int listening = socket(AF_INET, SOCK_STREAM, 0);
  if(listening == -1){
      std::cerr << "Can't create a socket!" << std::endl;
      return -1;
  }
  // Bind the socket to a IP / port
  sockaddr_in hint;
  hint.sin_family = AF_INET;
  hint.sin_port = htons(port); // htons means host to network short 
  inet_pton(AF_INET, ip, &hint.sin_addr);  

  if (bind(listening, (sockaddr*)&hint, sizeof(hint)) == -1){
      std::cerr << "Can't bind to IP/port" << std::endl;
      return -2;
  }

  // Mark the socket for listening
  if ((listen(listening, SOMAXCONN)) == -1){
      std::cerr << "Can't listen!" << std::endl;
      return -3;
  }

  // Accept a call
  sockaddr_in client;
  socklen_t clientSize = sizeof(client);
  char host[NI_MAXHOST];
  char svc[NI_MAXSERV];

  clientSocket = accept(listening, 
                          (sockaddr*)&client, 
                          &clientSize);

  if (clientSocket == -1){
      std::cerr << "Problem with client connecting!" << std::endl;
      return -4;
  }

  // Close the listening socket
  close(listening);

  memset (host , 0, NI_MAXHOST);
  memset (svc, 0, NI_MAXSERV);

  int result = getnameinfo((sockaddr*)&client, 
                          sizeof(client),
                          host,
                          NI_MAXHOST,
                          svc,
                          NI_MAXSERV,
                          0);
  if (result){
      std::cout << host << " connected on " << svc << std::endl;
  }
  else {
      inet_ntop(AF_INET, &client.sin_addr, host, NI_MAXHOST);
      std::cout << host << " connected on " << ntohs(client.sin_port) << std::endl;
  }
  char buf [4096] = {0};
  memset(buf, 0, 4096);
  //char message[] = {'-','-','W','e','l','c','o','m','e',' ','t','o',' ','t','h','e',' ','s','e','r','v','e','r','-','-'};
  char message[] = "--Welcome To The Server--";
  send(clientSocket, message, sizeof(message) , 0);
  return 0;
}

void Connect::Listen(){                                         // Wait for a connection to be made at "port" and deal with the message
  // While receiving - display message, echo message
  char buf [4096];
  while(true){
    // Clear the buffer
    memset(buf, 0, 4096);
    // Wait for a message
    int bytesRecv = recv(clientSocket, buf, 4096, 0);
    if (bytesRecv == -1){
        std::cerr << "There was a connection issue" << std::endl;
        break;
    }
    if (bytesRecv == 0){
        std::cout << "The client disconnected" << std::endl;
        break;
    }

    // Get and Display message
    std::string data = std::string(buf, 0, bytesRecv);
    std::cout << "Received: " << data << std::endl;

    // Check for errors
    /* std::string hold[] = {data};
    std::string status_string = Connect::ErrorCheck(hold);
    char status[sizeof(status_string)+1];
    StringToCharArray(status_string, status);
*/
    // Pass message onto Transmitter

    // Send status to client
    char buf [4096] = {0};
    memset(buf, 0, 4096);
    char status[] = "GTG";
    send(clientSocket, status, sizeof(status), 0);
  }
}

void Connect::CloseConnection(){                                // Safely close port and exit program
  // Close socket
  close(clientSocket);
}

std::string Connect::ErrorCheck(std::string[]){                 // Create message to send back to client depending on the data received
  return "ERROR";
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

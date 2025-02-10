
#include <iostream> 
using namespace std;
#include "game.h"
#pragma comment(lib, "Ws2_32.lib")
#include <winsock2.h>
#include <ws2tcpip.h>
#define PORT 8080


int main() {
    WSADATA wsaData;
    SOCKET sock = INVALID_SOCKET;
    struct sockaddr_in server_addr;
    char buffer[1024] = {0};

    // Initialize Winsock
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        std::cerr << "WSAStartup failed\n";
        return 1;
    }

    // Create socket
    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) == INVALID_SOCKET) {
        std::cerr << "Socket creation failed: " << WSAGetLastError() << "\n";
        WSACleanup();
        return 1;
    }

    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);
    server_addr.sin_addr.s_addr = inet_addr("127.0.0.1");

    // Connect to the Python server
    if (connect(sock, (struct sockaddr*)&server_addr, sizeof(server_addr)) == SOCKET_ERROR) {
        std::cerr << "Connection failed: " << WSAGetLastError() << "\n";
        closesocket(sock);
        WSACleanup();
        return 1;
    }

    std::cout << "Connected to the server.\n";

    while (true) {
        // Send data to the Python server
        std::string message = "Hello from C++ client!";
        send(sock, message.c_str(), message.size(), 0);
        std::cout << "Message sent: " << message << std::endl;

        // Receive response from the server
        int valread = recv(sock, buffer, 1024, 0);
        if (valread > 0) {
            std::cout << "Received from server: " << buffer << std::endl;
            memset(buffer, 0, sizeof(buffer));
        }

        Sleep(1000);  // Wait for a second before sending the next message
    }

    closesocket(sock);
    WSACleanup();
    return 0;
}

/*
#include <iostream>
#include <winsock2.h>
#include <ws2tcpip.h>

using namespace std;

#pragma comment(lib, "Ws2_32.lib")  // Link the Ws2_32 library

#define PORT 8080

int main() {
    WSADATA wsaData;
    SOCKET server_fd, new_socket;
    struct sockaddr_in address;
    int addrlen = sizeof(address);
    char buffer[1024] = {0};

    // Initialize Winsock
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        std::cerr << "WSAStartup failed\n";
        return 1;
    }

    // Create a socket
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == INVALID_SOCKET) {
        std::cerr << "Socket failed: " << WSAGetLastError() << "\n";
        WSACleanup();
        return 1;
    }

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    // Bind the socket
    if (bind(server_fd, (struct sockaddr*)&address, sizeof(address)) == SOCKET_ERROR) {
        std::cerr << "Bind failed: " << WSAGetLastError() << "\n";
        closesocket(server_fd);
        WSACleanup();
        return 1;
    }

    // Listen for incoming connections
    if (listen(server_fd, 3) == SOCKET_ERROR) {
        std::cerr << "Listen failed: " << WSAGetLastError() << "\n";
        closesocket(server_fd);
        WSACleanup();
        return 1;
    }

    std::cout << "Waiting for a connection...\n";
    if ((new_socket = accept(server_fd, (struct sockaddr*)&address, &addrlen)) == INVALID_SOCKET) {
        std::cerr << "Accept failed: " << WSAGetLastError() << "\n";
        closesocket(server_fd);
        WSACleanup();
        return 1;
    }
    int i = 0;
    while (i<15) {
        i++;
        // Send data to the Python client
        std::string message = "Hello from C++ server! " + to_string(i);
        send(new_socket, message.c_str(), message.size(), 0);
        std::cout << "Message sent: " << message << std::endl;

        // Receive data from the client
        int valread = recv(new_socket, buffer, 1024, 0);
        if (valread > 0) {
            std::cout << "Received from client: " << buffer << std::endl;
            memset(buffer, 0, sizeof(buffer));
        }

        Sleep(1000);  // Wait for a second before sending the next message
    }

    closesocket(new_socket);
    closesocket(server_fd);
    WSACleanup();
    return 0;
}
*/
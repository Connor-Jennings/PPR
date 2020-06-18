# Connor Jennings
# June/2020
# Makefile

#Use the g++ compiler
CC=clang++

#Compile time flags
CFLAGS = -std=c++17 -Wall -pedantic -O0 -c -fexec-charset=UTF-8

all : Server

Server : Server.o Main.o
	$(CC) Server.o Main.o -o Server

Server.o : Server.cpp
	$(CC) $(CFLAGS) Server.cpp -o Server.o

Main.o : Main.cpp
	$(CC) $(CFLAGS) Main.cpp -o Main.o

clean:
		rm -rf *o Server

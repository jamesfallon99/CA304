import socket #Imorting the socket library so sockets can be used
#A socket is just a point of communication
#Both the client and server will have to open a socket for communication to occur
import sys #Allow command line arguments to be used
from threading import Thread#Using threads allows the code to run concurrently. e.g waiting for incoming connections and handling that client at the same time

#Read through https://medium.com/swlh/lets-write-a-chat-app-in-python-f6783a9ac170 this article in order to understand how to go about this assingment.

#The handle_client function, puts all the connecting clients into their resepective chatrooms.
#It then handles the communication between the clients in their chatrooms
#By creating an infinite while loop, this function will always wait for incoming messages from the client
#Once a message is received from the client, it checks if this is an "exit" message, if it isn't it will broadcast the message, otherwise it deletes the client from the dictionary and closes the connection
def handle_client(client, username, chatroom):#Takes client socket, username and chatroom as arguments
    if chatroom not in client_dictionary: #If the client's chatroom name is not in the dictionary:
        client_dictionary[chatroom] = [] #Map the client's chatroom name to an empty list
        client_dictionary[chatroom].append(client) #Append this client to the list
    else:
        client_dictionary[chatroom].append(client) #If the chatroom name is already there, just append the client

    while True:#Create an infinite loop to handle all other communiaction from the client
        msg = client.recv(1024)#receive the message
        if msg != bytes("{exit}", "utf-8"):#If the message doesn't equal "exit"
            broadcast(msg, client, chatroom, username + ": ")#broadcast to all clients
        else:
            for connection in client_dictionary[chatroom]:#Loop through the list of clients
                if connection == client:#When it finds the connection
                    client_dictionary[chatroom].remove(connection) #Delete it from the dictionary
            client.close() #Close the connection. This frees up the ports so other applications can use them
            broadcast(bytes("{} has left the chat".format(username), "utf-8"), client, chatroom) #Tell all other connected clients that that client has left the chat
            break #break out of the loop
    

#The broadcast function is used to send a message to all clients in the chatroom
#Loops through the list of clients in the chatroom
#Sends the message to all clients in that chatroom
def broadcast(msg, client, chatroom, prefix=""): #prefix is for name identification so all other clients can see who sent the message
    for socket in client_dictionary[chatroom]:#Broadcast a message to all clients connected to the chatroom
        if socket != client:#Don't want to send the message to itself so check that before sending
            socket.send(bytes(prefix, "utf8")+msg) #Send the message

if __name__ == "__main__":
    
    client_dictionary = {}#maps a chatroom to a list of clients, each key(chatroom) acts as a different chatroom

    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #We have told the OS we are looking to open up a TCP socket using the IPv4 addressing protocol. TCP is a transport-layer protocol. It governs how the data is sent from one point to another. TCP guarantees reliable delivery.
    #Now we have a socket open
    #The server has a bit more setup to do before it can handle incoming connections
    #It needs to bind to an address
    #It needs to listen for incoming connections
    #It needs to accept connection requests
    if len(sys.argv) != 3:
        my_ip = "0.0.0.0" #If no command line arguments are supplied, default to this ip and port
        my_port = 8080 #Ports are how a computer determines which application is looking for data. Picking a large number as reserved ports are usually the lower numbers
        socket.bind((my_ip, my_port)) #It needs to bind to an address. Need to tell the socket what address we will be listening on and what port
        #We need to give an address because computers can have many network cards, this results in them having many IP addresses

    else:
        my_ip = sys.argv[1] #First command line argument is the ip address to run off
        my_port = int(sys.argv[2]) #The second command line argument is the port to listen on
        socket.bind((my_ip, my_port))
    print("Server started on {}:{}".format(my_ip, my_port))

    socket.listen()#Allow the socket to start waiting for connections

    #Now we need to allow for accepting connections
    while True:#Infinite loop that waits forever for incoming connections
        client, client_address = socket.accept() #This returns a connection object(client) and the address of the machine making the connection(client address)
        #Call socket.accept() to accept a connection
        client.send(bytes("Connected to {}:{}".format(my_ip, my_port), "utf-8")) #Sending a message directly to the client. To send data you can use send
        client.send(bytes("Type {exit} to exit the chatroom", "utf-8")) #Sending a message directly to the client. To send data you can use send

        username = client.recv(1024).decode("utf-8")#receive the client's username
        chatroom = client.recv(1024).decode("utf-8")#receive the client's chatroom name
        #To receive data we use the recv function
        #We must pass in the number of bytes we wish to receive at once
        #This should be a power of 2

        print(username + " connected to the server")
        print(username + " entered chatroom " + chatroom)
        Thread(target=handle_client, args=(client, username, chatroom)).start()#Creates a thread to allow this infinite loop to run concurrently with the handle_client() function. This allows for incoming connections and dealing with client's messages simultaneously


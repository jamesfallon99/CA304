import socket #Imorting the socket library so sockets can be used
import sys #Allow command line arguments to be used
from threading import Thread #Using threads allows the code to run concurrently

#The send_message function allows a client to send a message to the server
#We create an infinite while loop that will constantly allow a client to send a message(once they press enter the message will send)
def send_message():
        while True:#Infinite loop that will always allow a client to send their own message to another the server
            try:
                message = input() #Allows the client to send a message, when they press enter the message is sent
                client_socket.send(message.encode("utf-8")) #Send the message
            except OSError:
                break
#The receive_message function allows a client to receive a message from the server
#We create an infinite while loop that will constantly wait for a message to be received
#Once it is received, the message is displayed to the client
def receive_message():
    while True:#Infinite loop that will always receive messages when they are sent and allow a client to send their own message to another client
        try:
            msg = client_socket.recv(1024).decode("utf-8")#the recv() is the blocking part. It stops execution until it receives a message. This message is sent from one client to the server and displayed to another client
            print(msg)#Display this message to the client
        except OSError:
            break


if __name__ == "__main__":

    client_socket = socket.socket()
    #Now we have a socket open

    username = sys.argv[1] #Username will be the first command line argument
    host_ip = sys.argv[2]#IP address will be the 2nd command line argument
    host_port = int(sys.argv[3])#Port number will be the 3rd command line argument
    chatroom = sys.argv[4]#chatroom name will be the 4th command line argument

    client_socket.connect((host_ip, host_port))
    connect = client_socket.recv(1024).decode("utf-8") #Tells the client they are connected to the server. This message has been sent from the server and the client receives it.
    how_to_exit = client_socket.recv(1024).decode("utf-8")#Tells the client how to exit the chat. This message has been sent from the server and the client receives it.
    print(connect)
    print(how_to_exit)
    print("\n")
    client_socket.send(username.encode("utf-8"))#Send the username to the server
    client_socket.send(chatroom.encode("utf-8"))#Send the chatroom name to the server
    
    Thread(target=send_message).start() #These two threads allows a client to send a message and receive a message at the same time
    Thread(target=receive_message).start()
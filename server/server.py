"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time

# Global Constants
HOST = 'localhost'
PORT = 5500
BUFSIZ = 512
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

#Global Variables
clients = []


class Person():
    def __init__(self, addr, client_socket):
        self.addr = addr
        self.client_socket = client_socket
        self.name = None

    def set_name(self, name):
        self.name = name
    
    def __repr__(self):
        return f"Person({self.addr}, {self.name})"
    

def broadcast(msg, name,  prefix=""):
    """Broadcasts a message to all the clients."""

    # encode the message to bytes that we got from the client_communicaiton function
    encoded_msg = bytes(prefix, "utf8") + bytes(msg, "utf8") if isinstance(msg, str) else msg

    # each person is a socket object
    for person in clients:
        try:
            if "has joined the chat" in msg or "has left the chat" in msg:
                person.client_socket.send(encoded_msg)
            else:
                person.client_socket.send(bytes(name + ": ", "utf8") + encoded_msg)
        except:
            clients.remove(person)  # Remove disconnected clients


def client_communication(client):
    """Takes client socket object as argument."""
    try:
        client.client_socket.send("Welcome to the chat! Now type your name and press enter!".encode("utf8"))
        name = client.client_socket.recv(BUFSIZ).decode("utf8")
        client.set_name(name)

        #broadcasts that someone has joined the chat
        msg = f"{name} has joined the chat!"
        broadcast(msg, name)
        print(f"[CONNECTION] {name} connected to the chat.")

        while True: 
            # msg is the message sent by the client
            msg = client.client_socket.recv(BUFSIZ).decode("utf8")
            # print(f"{name}: {msg}")

            if msg == "{quit}": # if message is quit disconnect the client
                # client.client_socket.send(bytes("{quit}, utf8"))
                broadcast(f"{name} has left the chat.")
                clients.remove(client)
                client.client_socket.close()
                break

            else: # broadcast the message to all the clients
                broadcast(msg, name)
    
    except:
        print(f"[DISCONNECT] {name} disconnected unexpectedly")  # Show unexpected disconnects
        # broadcast(f"{name} has disconnected.", name)
    finally:
        if client in clients:
            clients.remove(client)
            client.client_socket.close()




def wait_for_connection(SERVER):
    """Wait for incoming connections.
    Accepts incoming connections
    starts a new thread to handle each client.
    """
    while True:
        try:
            # client_socket is the new socket object usable to send and receive data on the connection
            client_socket, client_address = SERVER.accept()
            print(f"%s:%s has connected to the server at {time.time()}. \n" % client_address)
            # client.send("Greetings from the cave! Now type your name and press enter!".encode("utf8"))
            
            person = Person(client_address, client_socket)
            clients.append(person)

            Thread(target=client_communication, args=(person,)).start()
        except:
            print("Error occurred!")
            break
    
    print("Server is shutting down.")


if __name__ == "__main__":
    SERVER.listen(5)  # Listens for 5 connections at max.
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=wait_for_connection, args=(SERVER,))
    ACCEPT_THREAD.start()  # Starts the infinite loop.
    ACCEPT_THREAD.join()
    SERVER.close()
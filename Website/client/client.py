from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread, Lock
import time

# Global Constants
HOST = 'localhost'
PORT = 5500
ADDR = (HOST, PORT)
BUFSIZ = 512

# Global Variables
messages = []

class Client():
    def __init__(self, name):
        self.name = name
        self.messages = []  # Store messages for this client

    def get_messages(self):
        # Return all messages and clear the list
        new_messages = self.messages[:]
        self.messages = []
        return new_messages

    def send_message(self, message):
        # Simulate sending a message by appending it to the list
        self.messages.append(message)

    def receive_messages(self):
        """Handles receiving messages"""
        while True:
            try:
                msg = self.client_socket.recv(BUFSIZ).decode()
                self.lock.acquire()
                if not msg:  # Connection closed by server
                    print("Server connection closed")
                    break
                self.messages.append(msg)
                self.lock.release()
                print(msg)
            except Exception as e:
                if not self.client_socket._closed:  # Only print error if not intentionally closed
                    print(f'Error receiving message: {e}')
                break

    def start(self):
        # Start threads for sending and receiving
        receive_thread = Thread(target=self.receive_messages)
        receive_thread.start()
        self.send_message(self.name)
        while True:
            message = input()
            if not self.send_message(message):
                break

    def update_messages(self, new_messages):
        while True:
            time.sleep(0.1)
            self.lock.acquire()
            self.messages.extend(new_messages)
            self.lock.release()

            for msg in new_messages:
                print(msg)
                if msg == "{quit}":
                    break


def main():
    name = input("Enter your name: ")
    client = Client(name)
    client.start()

    new_messages = client.get_messages()


    # run = True
    # while run:
    #     message = input()
    #     if not client.send_message(message):
    #         break


    client.update_messages(new_messages)
    
    
if __name__ == "__main__":
    main()



# # Set up the client socket
# client_socket = socket(AF_INET, SOCK_STREAM)
# client_socket.connect(ADDR)

# def receive_messages():
#     """Handles receiving messages"""
#     while True:
#         try:
#             msg = client_socket.recv(BUFSIZ).decode()
#             if not msg:  # Connection closed by server
#                 break
#             messages.append(msg)
#             print(msg)
#         except Exception as e:
#             if not client_socket._closed:  # Only print error if not intentionally closed
#                 print(f'Error receiving message: {e}')
#             break

# def send_message(msg):
#     """Handles sending a single message"""
#     if msg == "{quit}":
#         send_message(f"{name} has left the chat.")
#         time.sleep(2)  # Wait for server response
#         client_socket.close()
#         return False
#     try:
#         client_socket.send(bytes(msg, "utf8"))
#         return True
#     except:
#         return False

# # # Start threads for sending and receiving
# receive_Thread = Thread(target=receive_messages)
# receive_Thread.start()

# # send_thread = Thread(target=send_messages)
# # send_thread.start()

# name = input("Enter your name: ")
# send_message(name)

# send_message("Hello")


# while True:
#     message = input()
#     if not send_message(message):
#         break

# # time.sleep(3)
# # send_message("{quit}")




# # # Start threads for sending and receiving
# # receive_thread = Thread(target=receive_messages)
# # receive_thread.start()
# # send_thread = Thread(target=send_messages)
# # send_thread.start()
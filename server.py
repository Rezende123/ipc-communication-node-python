import socket
import json
import os

socket_name = "/tmp/fridge.socket"

class EventMessages:
    def __init__(self, event_name, data):
        self.type = event_name
        self.data = data
        
    def serialize(self):
        json_data = json.dumps(self.__dict__) + ' \f'
        
        return json_data.encode()

class Server:
    def __init__(self):
        # Ensure that the file doesn't exist yet (or an error will be raised)
        if os.path.exists(socket_name):
            os.remove(socket_name)
            
        self.__server_socket = socket.socket( socket.AF_UNIX, socket.SOCK_STREAM )
        self.__server_socket.bind(socket_name)
        self.__server_socket.listen()
        
        connection, addr = self.__server_socket.accept()

        print ("Connection from: " + str(addr))
        while True:
            data = connection.recv(1024).decode()
            if not data:
                break
            print ("from connected  user: " + str(data))                                            
            data = str(data).upper()
            print ("Received from User: " + str(data))
            data = input("type message: ")
            
            message = EventMessages('message', data).serialize()
            
            print(message)
            
            connection.sendall(message)                                        
        connection.close()     

server = Server()
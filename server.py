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

class IpcSocket(socket.socket):
    def __object_init__(self, socket_obj):
        super().__init__(fileno=socket_obj.detach())
        return self

    def accept(self):
        con, cli = super().accept()
        return self.__object_init__(con), cli

    def emit(self, event_name, data):
        message = EventMessages(event_name, data).serialize()
        
        self.sendall(message)

    def format_input_data(self, data):
        data = data.decode("utf-8")
        data = data.replace('\f', '')
        data = json.loads(data)
        
        return data
        
    def on(self, event_name, callback):
        __data__ = self.recv(1024)
        __data__ = self.format_input_data(__data__)
        
        if __data__ and __data__["type"] == event_name:
            callback(__data__["data"])
            

class Server:
    def __init__(self):
        # Ensure that the file doesn't exist yet (or an error will be raised)
        if os.path.exists(socket_name):
            os.remove(socket_name)
            
        self.__server_socket = IpcSocket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.__server_socket.bind(socket_name)
        self.__server_socket.listen()
        
        self.connection, addr = self.__server_socket.accept()

        print ("Connection from: " + str(addr))
        
        self.connection.on( 'message', self.readMessage )
        
        print("Waiting...")
        
    def readMessage(self, data):
        if data is None:                     
            self.connection.close()
        print ("from connected  user: " + str(data))                                            
        data = str(data).upper()
        print ("Received from User: " + str(data))
        data = input("type message: ")
        
        self.connection.emit('message', data)                     
        self.connection.close()

server = Server()
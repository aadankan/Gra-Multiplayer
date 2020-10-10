import socket
import pickle


class Network:
    def __init__(self):
        # Basic for socket package
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Address to server
        self.server = "217.144.222.58"
        # Port to use
        self.port = 5050
        # Type of coding
        self.format = "UTF-8"
        # Message to disconnect (for the future)
        self.disconnect_message = "!DISCONNECTED"
        # Combine server address and used port
        self.addr = (self.server, self.port)
        # Making a connection and sending basic data
        self.connection = self.connect()

    # Function to receive start data
    def connect(self):
        try:
            # Making a connection
            self.client.connect(self.addr)
            # Receive start data
            return pickle.loads(self.client.recv(2048))
        except:
            pass

    # Function to send and receive data
    def send(self, data):
        try:
            # Sending data
            self.client.send(pickle.dumps(data))
            # Receive answer
            return pickle.loads(self.client.recv(2048))
        # Show error
        except socket.error as e:
            print(e)

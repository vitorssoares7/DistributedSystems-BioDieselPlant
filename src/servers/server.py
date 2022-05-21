import socket

class Server():
    def __init__(self, host, port, name=''):
        self.host = host
        self.port = port
        self.name = name
        self.socket = ""
        self.initSocket()
        #self.connect()

    def initSocket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(100)

        print(f'{self.name} server listening on port: ' + str(self.port))


    def connect(self):
        """
            now it accepts connections 
        """
        conn, addr = self.socket.accept()
        print('\n' + str(self.addr) + ' connected')
        return conn, addr


    def closeServer(self):
        #closes server's socket
        self.socket.close()
import socket
import sympy

class ServerHelper:
    @staticmethod
    def waitMessage(conn, prefix=''):
        """
            function to handle and wait message from the client
        """
        if prefix != '':
            conn.sendall(prefix.encode())
        message = conn.recv(1024).decode()   
        return message

    @staticmethod
    def sendMessage(conn, message):
        """
            function to handle and send messages to the client
        """
        message += '\n'
        conn.sendall(message.encode())

    @staticmethod
    def closeConnection(conn, addr):
        """
            function to close client connection
        """
        #conn.sendall('/end'.encode())
        conn.close()
        print('\n' + str(addr) + ' disconnected')

    @staticmethod
    def sendRequest(connection, message):
        """
            send a request for the other socket process
        """
        try:
            connection.sendall(bytes(message, encoding='utf-8'))
            response = connection.recv(1024)
            return response.decode()

        except Exception as error:
            print(error)
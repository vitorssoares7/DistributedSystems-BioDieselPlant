import socket
import time
import sys
from time import sleep

sys.path.append('../helpers')
from helpers.ports import OilTank
from helpers.helpers import ServerHelper
from helpers.enums import Substances, States

class OilTankServer:
    """
        Oil tank server class
    """
    def __init__(self):
        self.setServerProperties()

        self.oilAmount = 0
        self.state = States.Available

    def receiveOil(self, entry):
        """
            this function handles the entry of the oil tank
        """
        if self.state != States.Available:
            ServerHelper.sendMessage(self.conn, 'component is busy')
        else:
            if entry['substance'] == Substances.Oil:
                self.oilAmount += entry['amount']
                ServerHelper.sendMessage(self.conn, 'input received')
            else:
                ServerHelper.sendMessage(self.conn, 'invalid input')



    def transferOilToReactor(self):
        """
            this function transfer oil for the reactor every second
        """
        sendingAmount = 0
        if self.oilAmount > 0.75:
            sendingAmount = 0.75
        else:
            sendingAmount = self.oilAmount
            
        request = {
            'substance': Substances.Oil,
            'amount': sendingAmount
        }

        # send request and get response
        response = True

        if response:
            self.oilAmount -= sendingAmount

            













    def setServerProperties(self):
        self.host = OilTank.Host()
        self.port = OilTank.Port()
        self.socket = ""
        self.createSocket()
        self.bindSocket()
        self.acceptConnection()

    def createSocket(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        except OSError as message:
            print('socket creation error: ' + str(message))

    def bindSocket(self):
        """
            binding our created socket to the ip and port 
        """
        try:
            self.socket.bind((self.host, self.port))
            self.socket.listen(100)

            print('server listening on port: ' + str(self.port))

        #auto reconnection every 3 seconds in case of errors
        except OSError as message:
            print('socket binding error: ' + str(message))
            print('retrying in 3 seconds...\n')
            time.sleep(3)
            self.bindSocket()


    def acceptConnection(self):
        """
            now it accepts connections 
        """
        self.conn, self.addr = self.socket.accept()
        print('\n' + str(self.addr) + ' connected')

    def closeServer(self):
        #closes server's socket
        self.socket.close()
from .server import Server

class OilTankServer(Server):
    def __init__(self, host, port, name):
        super().__init__(host, port, name)



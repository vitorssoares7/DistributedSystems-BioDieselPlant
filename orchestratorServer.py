from src.servers.server import Server

class OrchestratorServer(Server):
    def __init__(self, host, port, name):
        super().__init__(host, port, name)


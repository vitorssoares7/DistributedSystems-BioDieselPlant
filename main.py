from orchestratorServer import OrchestratorServer
from src.helpers import ports
from src.servers.oilTankServer import OilTankServer

import threading

def main():
    global instances
    global threads

    instances = []
    threads = {}

    orchestrator = OrchestratorServer(ports.Orchestrator.Host(), ports.Orchestrator.Port(), 'Orchestrator')

    instances.append(OilTankServer(ports.OilTank.Host(), ports.OilTank.Port(), 'Oil Tank'))


    for server in instances:
        threads[server.name] = threading.Thread(target=server.connect(), args=())
        threads[server.name].start()


main()
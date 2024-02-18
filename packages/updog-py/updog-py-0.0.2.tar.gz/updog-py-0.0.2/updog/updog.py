from .logger import Logger
from .server import Server
from threading import Timer
from flask import Flask, request, jsonify

class Updog:
    Serverpool: list = []
    me: Server
    ClusterMaster: str = ""
    Master: bool = True
    Services: list = []
    serviceTimer: Timer
    slaveTimer: Timer
    log: Logger
    app = Flask(__name__)

    def __init__(self, Serverpool, Master, Services, Logger, port) -> None:
        self.Serverpool = Serverpool
        self.Master = Master
        self.Services = Services
        self.log = Logger
        if not self.Master:
            self.anounceSlave()
        self.log.dev_log("Updog instance created")

        self.app.route('/updog', methods=['GET', 'POST'])(self.updog)
        self.app.route('/getServerpool', methods=['GET'])(self.get_Serverpool)
        self.app.run(port=port)

    def updog(self):
        if request.method == 'POST':
            if request.json:
               data = request.json
               if data["type"] == "server":
                   server = Server(data["url"], data["port"])
                   self.addServer(server)
               else:
                   self.log.error_log("Invalid request")
                   return "Invalid request"
            else:
                self.log.error_log("Invalid request")
                return "Invalid request"

        elif request.method == 'GET':
            return "Status: OK"
        return "Updog"

    def get_Serverpool(self) -> jsonify:
        return jsonify(Serverpool=[e.serialize() for e in self.Serverpool])

#TODO
    def anounceSlave(self) -> None:
        self.log.info_log("Slave anounced")

#TODO
    def anounceMaster(self) -> None:
        pass

#TODO
    def anounceServerpool(self) -> None:
        pass

    def addServer(self, server: Server) -> None:
        self.Serverpool.append(server)
        self.orderServerpool()
        self.anounceServerpool()

    def removeServer(self, server) -> None:
        self.Serverpool.remove(server)

    def addService(self, service) -> None:
        if not callable(service.run()):
            return

        if service not in self.Services:
            self.Services.append(service)

    def removeService(self, service) -> None:
        if not callable(service):
            return

        if service in self.Services:
            self.Services.remove(service)

    def setMaster(self, master: bool) -> None:
        self.Master = master

    def getMaster(self) -> bool:
        return self.Master

    def getServerpool(self) -> list:
        return self.Serverpool

    def getServices(self) -> list:
        return self.Services

    def promoteSlave(self) -> None:
        if self.me.getRank() == 1:
            self.Master = True
            self.orderServerpool()
            self.anounceMaster()
        self.log.error_log("Cant promote slave, not next in line")

    def orderServerpool(self) -> None:
        for i, server in enumerate(self.Serverpool):
           server.setRank(i)

    def demoteMaster(self) -> None:
        self.Master = False

    def runServices(self) -> None:
        for service in self.Services:
            self.log.dev_log("Running service: " + service.__str__())
            res = service.run()
            self.log.dev_log("Service: " + service.__str__() + " returned: " + str(res))

    def checkSceduler(self, time: int) -> None:
        self.serviceTimer = Timer(time, self.checkSceduler)
        self.runServices()

    def checkServerpool(self) -> None:
        for server in self.Serverpool:
           self.log.dev_log("Checking server: " + server)
           res = server.checkServer()
           if res == False:
               self.notify("Server down", server.getIP() + " war master= " + server.getMaster())
               self.removeServer(server)
               self.orderServerpool()
               if server.getMaster() == True:
                   self.promoteSlave()
                   server.setMaster(False)

#TODO
    def notify(self, info: str, msg: str) -> None:
        pass

    def slaveSceduler(self, time: int) -> None:
        self.slaveTimer = Timer(time, self.slaveSceduler)
        self.checkServerpool()

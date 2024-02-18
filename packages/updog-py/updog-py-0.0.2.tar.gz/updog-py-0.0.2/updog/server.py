from urllib.request import urlopen, Request

class Server:
    ip: str
    port: int = 80
    master: bool = False
    rank: int = 99

    def __init__(self,  ip: str, port: int):
        self.ip = ip
        self.port = port

    def getIP(self) -> str:
        return self.ip

    def setMaster(self, master: bool) -> None:
        self.master = master
        self.rank = 0

    def getMaster(self) -> bool:
        return self.master

    def setRank(self, rank: int) -> None:
        self.rank = rank

    def getRank(self) -> int:
        return self.rank

    def checkServer(self) -> bool:
        try:
            res = urlopen(self.ip + ":" + str(self.port))
            if res.status == 200:
                return True
            return False
        except Exception as e:
            return False

    def serialize(self) -> dict:
        return {
            "ip": self.ip,
            "port": self.port,
            "master": self.master,
            "rank": self.rank
        }

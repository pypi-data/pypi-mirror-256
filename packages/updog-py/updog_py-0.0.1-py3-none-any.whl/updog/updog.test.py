import os
import updog
from logger import Logger

# Create a new updog instance
os.environ["ENVIROMENT"] = "test"
log = Logger()
def service1():
    print("Service 1")

def service2():
    print("Service 2")

def service3():
    print("Service 3")

Serverpool = ["server1", "server2", "server3"]
Services = [service1, service2]
test = updog.Updog(Serverpool, True, Services, log)
test.runServices()
test.checkServerpool()

def test_getServerpool():
    assert test.getServerpool() == ["server1", "server2", "server3"]

def test_getServices():
    assert test.getServices() == [service1, service2]

def test_addServer():
    test.addServer("server4")
    assert test.getServerpool() == ["server1", "server2", "server3", "server4"]

def test_removeServer():
    test.removeServer("server4")
    assert test.getServerpool() == ["server1", "server2", "server3"]

def test_addService():
    test.addService(service3)
    assert test.getServices() == [service1, service2, service3]

def test_removeService():
    test.removeService(service1)
    assert test.getServices() == [service2, service3]
    test.removeService(service3)
    assert test.getServices() == [service2]

def test_fail_addService():
    test.addService("service3")
    assert test.getServices() == [service2]

def test_setMaster():
    test.setMaster(False)
    assert test.getMaster() == False

def test_getMaster():
    assert test.getMaster() == False

def test_promoteSlave():
    test.promoteSlave()
    assert test.getMaster() == True

def main():
    test_getServerpool()
    test_getServices()
    test_addServer()
    test_removeServer()
    test_addService()
    test_removeService()
    test_setMaster()
    test_getMaster()
    test_promoteSlave()
    log.dev_log("All tests passed")

if __name__ == "__main__":
    main()

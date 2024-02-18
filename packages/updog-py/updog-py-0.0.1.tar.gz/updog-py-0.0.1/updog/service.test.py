from Service import Service
from PostgreSQLBuilder import PostgreSQLBuilder
from HTTPGetBuilder import HTTPGetBuilder

def printRes(result):
    print(result)
    return "asd"

if __name__ == "__main__":
    builder = PostgreSQLBuilder()
    builder.connect("user", "password", "host", 5432, "database")
    builder.query("SELECT * FROM table")
    service = Service(builder)
    service.run()

    builder = HTTPGetBuilder(url="http://www.google.com", onlystatus=True)
    service = Service(builder)
    service.setResFunc(printRes)
    print(service.run())
    print("Service ran")


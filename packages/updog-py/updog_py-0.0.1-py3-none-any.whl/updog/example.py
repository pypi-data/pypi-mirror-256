from updog import Updog
from logger import Logger
from PostgreSQLBuilder import PostgreSQLBuilder
from HTTPGetBuilder import HTTPGetBuilder
from Service import Service
from server import Server
import os

os.environ["ENVIROMENT"] = "dev"


log = Logger()

sql = PostgreSQLBuilder()
sql.connect("user", "password", "host.email", 5432, "database")
sql.query("SELECT * FROM table")
service1 = Service(sql)
print(service1.__str__())

port = 1234
server1 = Server("google.com", 80)

updog = Updog([server1], True, [service1], log)

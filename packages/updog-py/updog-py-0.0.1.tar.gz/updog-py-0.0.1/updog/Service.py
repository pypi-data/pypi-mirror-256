from .builder import PostgreSQLBuilder, HTTPGetBuilder
from typing import TypeVar

T = TypeVar('T', PostgreSQLBuilder, HTTPGetBuilder)

class Service:
    builder: T
    resFunc = None

    def __init__(self, builder: T) -> None:
        self.builder = builder

    def setResFunc(self, resFunc) -> None:
        if not callable(resFunc):
            return
        self.resFunc = resFunc

    def run(self) -> bool:
        result = self.builder.execute()
        if self.resFunc:
            return self.resFunc(result)
        else:
            if result:
                return True
            else:
                return False

    def __str__(self) -> str:
        return f"Service: {self.builder.__str__()}"

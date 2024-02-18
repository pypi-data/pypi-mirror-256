import os
Enviroment = os.getenv("ENVIROMENT")

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Logger:
    def __init__(self):
        self.Enviroment = os.getenv("ENVIROMENT")

    def dev_log(self, message):
        if self.Enviroment == "dev" or self.Enviroment == "test":
            print(f"{bcolors.OKBLUE} {message} {bcolors.ENDC}")

    def error_log(self, message):
        print(f"{bcolors.FAIL} {message} {bcolors.ENDC}")

    def warning_log(self, message):
        print(f"{bcolors.WARNING} {message} {bcolors.ENDC}")

    def info_log(self, message):
        print(f"{bcolors.OKBLUE} {message} {bcolors.ENDC}")

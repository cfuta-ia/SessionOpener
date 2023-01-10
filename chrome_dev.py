#!venv/bin/python3

#from .manager import Manager

from framework.util.manager import Manager

manager = Manager()

manager.startBrowser()
for _ in range(3):
    manager.addSession()
manager.removeSession()
manager.addSession()
try:
    b = 1/0
except Exception as exp:
    print(exp)

inp = input()
manager.terminate()
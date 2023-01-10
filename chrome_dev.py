#!venv/bin/python3

#from .manager import Manager

from framework.util.manager import Manager

manager = Manager()

manager.startBrowser()
for _ in range(3):
    manager.addSession()
manager.removeSession()
manager.addSession()

inp = input()
manager.terminate()
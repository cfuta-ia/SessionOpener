#!venv/bin/python3

#from .manager import Manager

from framework.util.manager import Manager
from framework.util.manager import Operator
from time import sleep

if 1==0:
    manager = Manager()

    manager.startBrowser()

    manager.addSession()
    #manager.removeSession()
    #manager.addSession()

    sleep(8)
    manager.terminate()
else:
    operator = Operator()
    operator.setDeviceConfig('localhost', '8088')
    print(operator.device)
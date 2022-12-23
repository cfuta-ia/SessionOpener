#!venv/bin/python3

# Imports
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
#from selenium.webdriver import Firefox
#from selenium.webdriver.firefox.service import Service
from .counter import SessionCount
from .status import Status
from .functions import getOS

# Client Opener Manager
class Manager:
    """Client opener manager class, takes in commands to add/delete a 
    new client session or terminate the whole browser"""
    _servicePath = "./venv/bin/geckodriver"
    def __init__(self):
        """Starts a browser session on manager & opens first session"""
        self.driver = None
        self.client = None
        self.counter = SessionCount()
    
    @property
    def driver_config(self):
        """Function get the os of the system and return the args for the selenium driver"""
        return {'service': Service(self._servicePath)}

    def startBrowser(self, deviceIP='localhost', devicePort='8088'):
        """Initialize manager -- start the browser & set the browser client"""
        if self.driver:
            status = self.getManagerStatus(Status.BROWSER_EXISTS)
        else:
            #self.driver = Firefox(**self.driver_config)
            self.driver = Chrome(ChromeDriverManager().install())
            self.setClientAttributes(deviceIP, devicePort)
            self.client.newSession(self.driver, newTab=False)
            self.counter.setCount(self.getTabCount())
            status = self.getManagerStatus(Status.GOOD)
        return status
    
    def endBrowser(self):
        """Quit out of the entire driver (browser), quits the entire browser session"""
        if self.driver:
            self.driver.quit()
            status = self.getManagerStatus(Status.TERMINATE_SUCCESS)
            self.driver = None
            self.client = None
            self.counter.reset
        else:
            status = self.getManagerStatus(Status.NO_BROWSER)
        return status
    
    def terminate(self):
        """Terminate the browser"""
        if self.driver:
            self.driver.quit()
        
    def addSession(self):
        """Add new session through the client class"""
        if self.driver:
            self.client.newSession(self.driver)
            self.counter.setCount(self.getTabCount())
            status = self.getManagerStatus(Status.GOOD)
        else:
            status = self.getManagerStatus(Status.NO_BROWSER)
        return status

    def removeSession(self):
        """Remove the latest session added to the driver (browser)"""
        if self.driver:
            if self.getTabCount() == 1:
                status = self.getManagerStatus(Status.CANNOT_REMOVE)
            else:
                self.driver.close()
                self.driver.switch_to.window(self.getTabID())
                self.counter.setCount(self.getTabCount())
                status = self.getManagerStatus(Status.GOOD)
        else:
            status = self.getManagerStatus(Status.NO_BROWSER)
        return status
    
    def getTabID(self, index=-1):
        """Get the tab by index in the browser"""
        return self.driver.window_handles[index]
    
    def getTabCount(self):
        """Get the current count of open tabs"""
        return len(self.driver.window_handles)
    
    def getManagerStatus(self, state):
        """Get the manager status to be returned by the manager functions"""
        return {'benchmark': self.counter.toDict, 'status': state.value}

    def setClientAttributes(self, deviceIP, devicePort):
        """Set the client attributes such as IP address and port for the device gateway being tested"""
        self.client = self.Client(ip=deviceIP, port=devicePort)
        return None

    class Client:
        """Client opener class to open the client url in the supplied driver"""
        def __init__(self, protocol='http', ip='localhost', port='8088', project='SessionOpener', view=''):
            """Opens a new client session on the input driver
            
            Args:
                driver: driver (browser) to open the session on
                newTab: boolean to open new session on a new tab or not
            """
            self._deviceURL(protocol=protocol, ip=ip, port=port, project=project, view=view)

        def newSession(self, driver, newTab=True):
            """Function to open a new session with the supplied driver and whether to open a new tab or not
            
            Args:
                driver: selenium driver that new client will be opened on
                newTab: boolean variable to open client on a new tab or not
            """
            if newTab:
                driver.switch_to.new_window('')
            #driver.get(self.deviceURL)
            driver.get('http://example.com')
            return None

        def _deviceURL(self, protocol, ip, port, project, view):
            """Generate the url string for the client to open from the device
            
            Args:
                protocol: http or https protocol to use for the client
                ip: device ip address to open the client with
                port: port the ignition gateway is running on
                project: name of the project on the device
                view: page to use for the client test
            """
            self.deviceURL = f"{protocol}://{ip}:{port}/data/perspective/client/{project}/{view}"
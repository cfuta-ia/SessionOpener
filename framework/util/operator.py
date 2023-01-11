#!venv/bin/python3

# Imports
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from .counter import SessionCount
from .status import Status
from time import sleep

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Driver Operator Class
class Operator:
    def __init__(self):
        self.setProperties()

    def addSession(self):
        """ """
        if self.device.get('configured', False):
            driver = Chrome(**self.driver_config)
            driver.get(self.device.get('url', 'http://www.example.com/'))
            self.browsers.append(driver)
            status = self.getStatus(Status.GOOD)
        else:
            status = self.getStatus(Status.NO_BROWSER)
        return status

    def removeSession(self):
        """ """
        if self.device.get('configured', False):
            if self.sessionCount > 1:
                status = self.getManagerStatus(Status.CANNOT_REMOVE)
            else:
                driver = self.browsers.pop()
                self.killDriver(driver)
                status = self.getStatus(Status.GOOD)
        else:
            status = self.getStatus(Status.NO_BROWSER)
        return status

    def endTesting(self):
        """ """
        status = self.getStatus(Status.TERMINATE_SUCCESS)
        for driver in self.browsers:
            self.killDriver(driver)
        self.setProperties()
        return status

    def killDriver(self, driver):
        """Convenience function to close a driver"""
        driver.quite()
        driver.close()
        return None
    
    # Properties
    @property
    def sessionCount(self):
        """Current tab count of the driver/browser"""
        return len(self.browsers)

    @property
    def driver_config(self):
        """Function get the os of the system and return the args for the selenium driver"""
        options = ChromeOptions()
        args = {'disable-infobars', 'enable-automation', '--disable-gpu', '--no-sandbox', '--disable-deb-shm-usage'} #--headless
        for arg in args: 
            options.add_argument(arg)
        return {'service': Service(ChromeDriverManager().install()), 'chrome_options': options}

    # Getter Methods
    def getStatus(self, state):
        """Get the manager status to be returned by the manager functions
        
        Args:
            state: status Enum with a message, boolean value as it's value
        """
        self.counter.setCount(self.sessionCount)
        return {'benchmark': self.counter.toDict, 'status': state.value}

    # Setter Methods
    def setDeviceConfig(self, deviceIP, devicePort):
        """ """
        self.device['deviceIP'] = deviceIP
        self.device['devicePort'] = devicePort
        self.device['url'] = "{protocol}://{deviceIP}:{devicePort}/data/perspective/client/{project}/{view}".format(**self.device)
        self.device['configured'] = True
        return None

    def setProperties(self):
        """ """
        self.browsers = list()
        self.counter = SessionCount()
        self.device = {'protocol': 'http', 'project': 'SessionOpener', 'view': '', 'configured': False}


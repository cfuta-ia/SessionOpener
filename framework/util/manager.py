#!venv/bin/python3

# Imports
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver import Firefox
from selenium.webdriver import FirefoxOptions

from .counter import SessionCount
from .status import Status
from time import sleep

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Client Opener Manager
class Manager:
    """Client opener manager class, takes in commands to add/remove a client session or terminate the whole browser."""
    WAIT_TIME = 2 # Action wait time
    def __init__(self):
        """Initial properties of the manager class"""
        self.setManagerProperties()
    
    # Browser Methods
    def startBrowser(self, deviceIP='0.0.0.0', devicePort='8088'):
        """Initialize manager -- start the browser & set the browser client
        
        Args:
            deviceIP: ip address of the device being tested
            devicePort: port that the device is running the gateway through
        """
        if self.driver:
            status = self.getManagerStatus(Status.BROWSER_EXISTS)
        else:
            self.driver = Chrome(**self.driver_config)
            self.setDeviceURL(deviceIP=deviceIP, devicePort=devicePort)
            self.driver.get(self.deviceURL)
            self.counter.setCount(self.tabCount)
            status = self.getManagerStatus(Status.GOOD)
        return status
    
    def endBrowser(self):
        """Quit out of the entire driver (browser), quits the entire browser session"""
        if self.driver:
            self.driver.quit()
            status = self.getManagerStatus(Status.TERMINATE_SUCCESS)
            self.setManagerProperties()
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
            currentWindowCount = self.tabCount
            self.driver.execute_script(f'''window.open("{self.deviceURL}");''')
            WebDriverWait(self.driver, self.WAIT_TIME).until(EC.number_of_windows_to_be(currentWindowCount + 1))
            self.driver.switch_to.window(self.driver.window_handles[-1])
            
            #self.newSession()
            #self.driver.execute_script('''window.open();''')
            #self.driver.switch_to.new_window()
            #sleep(self.WAIT_TIME)
            #self.driver.get(self.deviceURL)
            #self.setDriverFocus(-1)

            self.counter.setCount(self.tabCount)
            status = self.getManagerStatus(Status.GOOD)
        else:
            status = self.getManagerStatus(Status.NO_BROWSER)
        return status

    def removeSession(self):
        """Remove the latest session added to the driver (browser)"""
        if self.driver:
            if self.tabCount == 1:
                status = self.getManagerStatus(Status.CANNOT_REMOVE)
            else:
                self.closeSession()
                
                #self.setDriverFocus(-1)
                #self.driver.close()
                #self.setDriverFocus()
                
                self.counter.setCount(self.tabCount)
                status = self.getManagerStatus(Status.GOOD)
        else:
            status = self.getManagerStatus(Status.NO_BROWSER)
        return status

    def newSession(self, newTab=True):
        """Create a new client session in the open driver/browser
        
        Args:
            newTab: boolean for whether to open the deviceURL on a new tab (default: True)
        """
        if newTab:
            self.driver.switch_to.new_window()
            sleep(self.WAIT_TIME)
            #self.driver.implicitly_wait(self.WAIT_TIME)
        self.driver.get(self.deviceURL)
        self.setDriverFocus(-1)
        return None

    def closeSession(self):
        """Close the last browser tab opened"""
        self.driver.close()
        sleep(self.WAIT_TIME)
        self.setDriverFocus(-1)
        return None

    def newSession2(self):
        currentWindowCount = self.tabCount
        self.driver.execute_script(f'''window.open("{self.deviceURL}");''')
        WebDriverWait(self.driver, self.WAIT_TIME).until(EC.number_of_windows_to_be(currentWindowCount + 1))
        self.driver.switch_to.window(self.driver.window_handles[-1])
        return None

    # Properties
    # Other class properties include: driver, deviceURL, counter, & WAIT_TIME
    @property
    def tabCount(self):
        """Current tab count of the driver/browser"""
        return len(self.driver.window_handles) if self.driver else 0

    @property
    def driver_config(self):
        """Function get the os of the system and return the args for the selenium driver"""
        options = ChromeOptions()
        options.add_argument('start-maximized')
        options.add_argument('disable-infobars')
        return {'service': Service(ChromeDriverManager().install()), 'chrome_options': options}

    # Setter Methods
    def setDeviceURL(self, deviceIP, devicePort, protocol='http', project='SessionOpener', view=''):
        """Generate the url string for the device being tested and set as the 'deviceURL' property
            
        Args:
            deviceIP: device ip address to open the client with
            devicePort: port the ignition gateway is running on
            protocol: http or https protocol to use for the client (default: http)
            project: name of the project on the device (default: SessionOpener)
            view: page to use for the client test (default: '')
        """
        #url = f"{protocol}://{deviceIP}:{devicePort}/data/perspective/client/{project}/{view}"
        url = 'https://www.google.com/'
        self.deviceURL = url
        return None

    def setDriverFocus(self, tabIndex=0):
        """Function to set the current driver's focus to the specified tab (by index)"""
        if self.driver:
            self.driver.switch_to.window(self.getTabID(index=tabIndex))
        return None

    def setManagerProperties(self):
        """Set the properties for the manager class"""
        self.driver = None
        self.deviceURL = None
        self.counter = SessionCount()
        return None

    # Getter Methods
    def getManagerStatus(self, state):
        """Get the manager status to be returned by the manager functions
        
        Args:
            state: status Enum with a message, boolean value as it's value
        """
        return {'benchmark': self.counter.toDict, 'status': state.value}

    def getTabID(self, index=-1):
        """Get the tab by index in the browser
        
        Args:
            index: tab index to get the ID for
        """
        return self.driver.window_handles[index]
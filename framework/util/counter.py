#!venv/bin/python3

class SessionCount:
    """Session counter class to track the number of sessions opened throughout the client opener test"""
    _currentCount = 0
    _maxCount = 0
    def __init__(self):
        self.reset
    
    def setCount(self, value):
        """Set the counter variable current count"""
        self.currentCount = value
        self.isMax()

    @property
    def toDict(self):
        """Convert class variables into a dict format"""
        return self.__dict__

    def isMax(self):
        """Function to check if the current count is the max count"""
        if self.currentCount > self.maxCount:
            self.maxCount = self.currentCount

    @property
    def reset(self):
        """Initialize counter class variables"""
        self.currentCount = self._currentCount
        self.maxCount = self._maxCount
#!venv/bin/python3

# Imports
from flask import Flask
from flask import request
import os, signal
from .util.manager import Manager
import datetime

def start_service(ip=None, port=None):
    """Start the flask service
    
    Args:
        ip: ip address of the device being tested
        port: port the Ignition Gateway is using on the device
    Returns:
        flask app
    """
    app = Flask(__name__)
    app.manager = Manager()

    @app.route('/testing', methods=['POST'])
    def test():
        """API endpoint to test the flask server -- returns the current timestamp"""
        return {'timestamp': datetime.datetime.now()}

    @app.route('/startBrowser', methods=['POST'])
    def startBrowser():
        """API call to manager startBrowser function"""
        args = request.args
        if ('deviceIP' in args.keys()) and ('devicePort' in args.keys()) and (len(args.keys()) == 2):
            return app.manager.startBrowser()
        else:
            return {'benchmark': None, 'status': {'message': "Request object can only contain the keys: 'deviceIP' and 'devicePort'", 'value': False}}
    
    @app.route('/endBrowser', methods=['POST'])
    def endBrowser():
        """API call to manager endBrowser function"""
        return app.manager.endBrowser()

    @app.route('/addSession', methods=['POST'])
    def addSession():
        """API call to manager addSession function"""
        return app.manager.addSession()

    @app.route('/removeSession', methods=['POST'])
    def removeSession():
        """API call to manager removeSession function"""
        return app.manager.removeSession()

    @app.route('/shutdown', methods=['POST'])
    def shutdown():
        """API call to manager terminate function and shuts down the flask server"""
        app.manager.terminate()
        os.kill(os.getpid(), signal.SIGINT)
        return {'message': 'Shutting down...', 'value': True}
    return app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == "main":
    start_service()
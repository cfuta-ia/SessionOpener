#!venv/bin/python3

# Imports
from flask import Flask
from flask import request
import os, signal
from .util.manager import Manager

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
        """ """
        return {'value': 1}

    @app.route('/startBrowser', methods=['POST'])
    def startBrowser():
        """ """
        args = request.args
        if ('deviceIP' in args.keys()) and ('devicePort' in args.keys()) and (len(args.keys()) == 2):
            return app.manager.startBrowser()
        else:
            return {'benchmark': None, 'status': {'message': "Request object can only contain the keys: 'deviceIP' and 'devicePort'", 'value': False}}
    
    @app.route('/endBrowser', methods=['POST'])
    def endBrowser():
        """ """
        return app.manager.endBrowser()

    @app.route('/addSession', methods=['POST'])
    def addSession():
        """ """
        return app.manager.addSession()

    @app.route('/removeSession', methods=['POST'])
    def removeSession():
        """ """
        return app.manager.removeSession()

    @app.route('/shutdown', methods=['POST'])
    def shutdown():
        app.manager.terminate()
        os.kill(os.getpid(), signal.SIGINT)
        return {'message': 'Shutting down...', 'value': True}
    return app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == "main":
    start_service()
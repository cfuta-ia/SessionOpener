#!venv/bin/python3

# Imports
from enum import Enum

class Status(Enum):
    """Error Enum that is returned by Flask endpoints"""
    GOOD = {'message': 'No error', 'value': True}
    TERMINATE_SUCCESS = {'message': 'Browser terminated successfully', 'value': True}
    NO_BROWSER = {'message': 'Browser has not been started yet', 'value': False}
    BROWSER_EXISTS = {'message': 'Browser already exists, terminate the existing one to start a new test', 'value': True}
    CANNOT_REMOVE = {'message': 'Browser must have atleast one tab open', 'value': False}
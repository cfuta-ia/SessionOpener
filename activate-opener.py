#!venv/bin/python3
## Imports
import argparse
from framework.app import start_service

## Argument Parser
parser = argparse.ArgumentParser(description='Start/Stop flask benchmark service CLI.', add_help=True)

## Arguments
# Device IP
parser.add_argument('-ip', '--ip', action='store', help='IP address of the device to open clients on.', nargs='?', default='localhost')

# Device Port
parser.add_argument('-port', '--port', action='store', help='Port of the device the Ignition Gateway is running on.', nargs='?', default='8088')

# Input args as a dict
args = parser.parse_args().__dict__

# Run command
start_service(*args)
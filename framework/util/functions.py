#!venv/bin/python3
import platform

def getOS():
    """Get the os of the system this is running on -- used to decide the browser image to run on"""
    platform_decoder = {'linux': 'linux', 'windows': 'windows', 'darwin': 'mac'}
    platform_system = platform.system().lower()
    system = platform_decoder.get(platform_system, False)
    return system

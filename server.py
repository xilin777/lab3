import socket
import threading
import time

tuplespace = {} 
operationcount = {'total': 0, 'read': 0, 'get': 0, 'put': 0, 'error': 0} 
clientcount = 0 
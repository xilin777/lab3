import socket
import threading
import time

tuplespace = {} 
operationcount = {'total': 0, 'read': 0, 'get': 0, 'put': 0, 'error': 0} 
clientcount = 0 

def handleclient(clientsocket):
    global operationcount
    global clientcount
    clientcount += 1  
    try:
        while True:
            data = clientsocket.recv(1024).decode()  
            if not data: 
                break
            operationcount['total'] += 1 
            size = int(data[:3])  
            command = data[3] 
            
            
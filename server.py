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
            
            if command == 'R': 
                operationcount['read'] += 1 
                key = data[5:]  
                if key in tuplespace:  
                    value = tuplespace[key]  
                    response = f"{len(f'OK ({key}, {value}) read'):03d} OK ({key}, {value}) read"
                else:  
                    operationcount['error'] += 1  
                    response = f"{len('ERR no such key'):03d} ERR no such key" 
                    
            elif command == 'G': 
                operationcount['get'] += 1 
                key = data[5:]  
                if key in tuplespace:  
                    value = tuplespace.pop(key)  
                    response = f"{len(f'OK ({key}, {value}) get'):03d} OK ({key}, {value}) get"
                else:  
                    operationcount['error'] += 1 
                    response = f"{len('ERR no such key'):03d} ERR no such key" 
            elif command == 'P': 
                operationcount['put'] += 1  
                parts = data[5:].split(' ', 1)  
                key = parts[0]  
                value = parts[1]  
                if len(key) > 999 or len(value) > 999:  
                    operationcount['error'] += 1  
                    response = f"{len('ERR key or value too long'):03d} ERR key or value too long"
                else:  
                    tuplespace[key] = value  
                    response = f"{len(f'OK ({key}, {value}) put'):03d} OK ({key}, {value}) put"  
                            
            clientsocket.send(response.encode()) 
    except Exception as e:  
        print(f"Error handling client: {e}")
    finally:
        clientsocket.close()  
        clientcount -= 1  
        
def printsummary():
    while True:
        time.sleep(10)  
        tuplecount = len(tuplespace) 
        if tuplecount > 0:  
            totaltuplesize = sum(len(k) + len(v) for k, v in tuplespace.items())  
            averagetuplesize = totaltuplesize / tuplecount  
            totalkeysize = sum(len(k) for k in tuplespace.keys()) 
            averagekeysize = totalkeysize / tuplecount  
            totalvaluesize = sum(len(v) for v in tuplespace.values())  
            averagevaluesize = totalvaluesize / tuplecount 
        else:  
            averagetuplesize = 0
            averagekeysize = 0
            averagevaluesize = 0  
            
        print(f"Tuple count: {tuplecount}")  
        print(f"Average tuple size: {averagetuplesize}") 
        print(f"Average key size: {averagekeysize}")
        print(f"Average value size: {averagevaluesize}")  
        print(f"Total connected clients: {clientcount}")  
        print(f"Total operations: {operationcount['total']}")
        print(f"READ operations: {operationcount['read']}")  
        print(f"GET operations: {operationcount['get']}")  
        print(f"PUT operations: {operationcount['put']}")  
        print(f"Error operations: {operationcount['error']}")  
        
        
                        
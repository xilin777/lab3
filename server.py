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
            # Parse message length (NNN) and validate
            if len(data) < 5 or not data[:3].isdigit():
                operationcount['error'] += 1
                response = f"{len('ERR invalid format'):03d} ERR invalid format"
                clientsocket.send(response.encode())
                continue
            
            size = int(data[:3])  
            command = data[3] 
            
            if command == 'R': 
                operationcount['read'] += 1 
                key = data[6:]  
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
                    
            else:
                operationcount['error'] += 1
                response = f"{len('ERR unknown command'):03d} ERR unknown command"
                            
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
        
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:  
        print("Usage: python server.py <port>")
        sys.exit(1)
    port = int(sys.argv[1])  
    if port < 50000 or port > 59999:  
        print("Port must be between 50000 and 59999")
        sys.exit(1)     
        
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    serversocket.bind(('localhost', port))  
    serversocket.listen(5)  
    summarythread = threading.Thread(target=printsummary)  
    summarythread.daemon = True  
    summarythread.start()  
    print(f"Server listening on port {port}")   
    
while True:
        clientsocket, addr = serversocket.accept()
        client_thread = threading.Thread(target=handleclient, args=(clientsocket,))
        client_thread.start()
        

        
                        
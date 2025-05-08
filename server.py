#Import module
import socket
import threading
import time

#Define global variables
tuplespace = {} 
operationcount = {'total': 0, 'read': 0, 'get': 0, 'put': 0, 'error': 0}# Operation Count Statistics 
clientcount = 0 
lock = threading.Lock()#add lock to prevent concurrent access to tuplespace and operationcount

#Client processing function (initialization)
def handleclient(clientsocket):
    global operationcount
    global clientcount
    clientcount += 1 #Increments by 1 each time a new client connects 

#Receive client data    
    try:
        while True:
            data = clientsocket.recv(1024).decode()  # Receive data sent by the client
            if not data: 
                break
            with lock:
                operationcount['total'] += 1 
            # Parse message length (NNN) and validate
            if len(data) < 7 or not data[:3].isdigit():
                operationcount['error'] += 1
                response = f"{len('ERROR invalid format'):03d} ERROR invalid format"
                clientsocket.send(response.encode())
                continue
            
            size = int(data[:3])#The first three characters of the data are the length.  
            command = data[3] # The fourth character is the command type
            args = data[5:]
          
          #Process the READ command  
            if command == 'R': # If it is the READ command
                operationcount['read'] += 1 
                key = data[6:]  
                if key in tuplespace:  
                    value = tuplespace[key]  # Get the corresponding value
                    response = f"{len(f'OK ({key}, {value}) read'):03d} OK ({key}, {value}) read"
                else:  # If the key does not exist
                    operationcount['error'] += 1  
                    response = f"{len('ERROR no such key'):03d} ERROR no such key" 
          
           #Handle the GET command         
            elif command == 'G': # If it is a GET command
                operationcount['get'] += 1 
                key = data[6:]  
                if key in tuplespace:  
                    value = tuplespace.pop(key) #Delete the key-value pairs and get the values 
                    response = f"{len(f'OK ({key}, {value}) get'):03d} OK ({key}, {value}) get"
                else:  
                    operationcount['error'] += 1 
                    response = f"{len('ERROR no such key'):03d} ERROR no such key" 
            
            #Handle the PUT command
            elif command == 'P': # If it is the PUT command
                operationcount['put'] += 1  
                parts = data[6:].split(' ', 1)  
                key = parts[0]  
                value = parts[1]  
                if len(key) > 999 or len(value) > 999: # If the key or value is too long 
                    operationcount['error'] += 1  
                    response = f"{len('ERROR key or value too long'):03d} ERROR key or value too long"
                else:  # If the key and value are normal
                    tuplespace[key] = value  
                    response = f"{len(f'OK ({key}, {value}) put'):03d} OK ({key}, {value}) put"
                    
            else:
                operationcount['error'] += 1
                response = f"{len('ERROR unknown command'):03d} ERROR unknown command"
           
           #Send responses and handle exceptions                 
            clientsocket.send(response.encode()) # Send the response to the client
    except Exception as e:  
        print(f"Error handling client: {e}")
    finally:
       with lock:
        clientsocket.close()  # Close the client connection
        
         
#Statistical information printing function        
def printsummary():
    while True:
        time.sleep(10) # Print once every 10 seconds
        tuplecount = len(tuplespace) 
        if tuplecount > 0:  
            totaltuplesize = sum(len(k) + len(v) for k, v in tuplespace.items())  # Calculate the total size
            averagetuplesize = totaltuplesize / tuplecount # Calculate the average size 
            totalkeysize = sum(len(k) for k in tuplespace.keys()) # Calculate the total size of the keys
            averagekeysize = totalkeysize / tuplecount  # Calculate the average size of the keys
            totalvaluesize = sum(len(v) for v in tuplespace.values())# Calculate the total size of the values  
            averagevaluesize = totalvaluesize / tuplecount # Calculate the average size of the value
        else:  
            averagetuplesize = 0
            averagekeysize = 0
            averagevaluesize = 0  
        
        #Statistical information printing function    
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
 
 #main function       
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:  # Check the number of parameters
        print("Usage: python server.py <port>")
        sys.exit(1)
    port = int(sys.argv[1])  # Get the port number
    if port < 50000 or port > 59999:  # Check the port number range
        print("Port should be between 50000 and 59999")
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
        

        
                        
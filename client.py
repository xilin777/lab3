import socket
import sys

def send_request(sock, request):
    size = len(request) + 3  
    formatted_request = f"{size:03d}{request}"  
    sock.send(formatted_request.encode())  
    response = sock.recv(1024).decode()  
    print(f"Request: {request}, Response: {response}") 
    
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python client.py <host> <port> <request_file>")
        sys.exit(1) 

    host = sys.argv[1]  
    port = int(sys.argv[2])  
    request_file = sys.argv[3] 
    
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        client_socket.connect((host, port))
        
        with open(request_file, 'r') as file:  
            for line in file:  
                line = line.strip()  
                if line:  
                    parts = line.split() 
                    
                    if len(parts) == 2:  
                        command = parts[0]  
                        key = parts[1]  #
                        if command == 'R': 
                            request = f" R {key}"  
                        elif command == 'G':  
                            request = f" G {key}"  
                        else:
                            print(f"Invalid command: {command}") 
                            continue    
                        

                    elif len(parts) == 3:  
                        command = parts[0]  
                        key = parts[1]  
                        value = parts[2]  
                        if command == 'P':  
                            request = f" P {key} {value}"  
                        else:
                            print(f"Invalid command: {command}")  
                            continue  
                        
                    collated_size = len(key) + len(value) if command == 'P' else len(key)  
                    if collated_size > 970:  
                        print(f"Error: Collated size exceeds 970 characters. Ignoring request: {line}")  
                    else:
                        send_request(client_socket, request)  
                        
        client_socket.close()  
    except Exception as e:  
        print(f"Error: {e}") 
                        
                    
                    
        
       
                    
  
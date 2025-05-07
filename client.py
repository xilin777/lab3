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
                if not line:
                    continue
                parts = line.split() 
                command = parts[0]  
                if command not in ['R', 'G', 'P']:
                    print(f"Invalid command: {command}")
                    continue
                   
                if command in ['R', 'G']:
                    if len(parts) != 2:
                        print(f"Invalid parameters for {command} command")
                        continue
                    key = parts[1]
                    request = f" {command} {key}"  
                    collated_size = len(key)  
                    if collated_size > 970:  
                        print(f"Error: Collated size exceeds 970 characters. Ignoring request: {line}")
                        continue
                    send_request(client_socket, request)

                    
                if request:
                    collated_size = len(key) + len(value) if command == 'P' else len(key)  
                    if collated_size > 970:  
                        print(f"Error: Collated size exceeds 970 characters. Ignoring request: {line}")  
                    else:
                        send_request(client_socket, request)  
                        
        client_socket.close()  
    except Exception as e:  
        print(f"Error: {e}") 
                        
                    
                    
        
       
                    
  
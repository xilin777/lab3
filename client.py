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
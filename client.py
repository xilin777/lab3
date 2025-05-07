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
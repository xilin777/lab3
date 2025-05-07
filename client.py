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
                    
                    if len(parts) == 2:  # 如果是 READ 或 GET 请求
                        command = parts[0]  # 获取命令
                        key = parts[1]  # 获取键
                        if command == 'R':  # 如果是 READ 命令
                            request = f" R {key}"  # 构造请求
                        elif command == 'G':  # 如果是 GET 命令
                            request = f" G {key}"  # 构造请求
                        else:
                            print(f"Invalid command: {command}")  # 如果命令无效
                            continue  # 跳过当前行
                    
                    
        
       
                    
  
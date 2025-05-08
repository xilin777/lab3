import socket
import sys

def send_request(sock, request):
    request = request.strip() 
    command = request[0]     
    args = request[1:].strip() 
    formatted_request = f"{command} {args}" 
    size = len(formatted_request) + 3
    formatted_request = f"{size:03d}{formatted_request}"
    
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

        with open(request_file, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                parts = line.split()
                command = parts[0]

                command_mapping = {
                    'READ': 'R',
                    'GET': 'G',
                    'PUT': 'P'
                }
                if command not in command_mapping:
                    print(f"Invalid command: {command}")
                    continue
                command = command_mapping[command]

                if command in ['R', 'G']:
                    if len(parts) != 2:
                        print(f"Invalid parameters for {command} command")
                        continue
                    key = parts[1]
                    request = f" {command} {key}"
                    collated_size = len(key)
                    if collated_size > 999:
                        print(f"Error: Collated size exceeds 999 characters. Ignoring request: {line}")
                        continue
                    send_request(client_socket, request)

                elif command == 'P':
                    if len(parts) < 2:
                        print(f"Invalid parameters for {command} command")
                        continue
                    key = parts[1]
                    value = " ".join(parts[2:])
                    collated_size = len(f"{key} {value}")
                    if collated_size > 999:
                        print(f"Error: Collated size exceeds 999 characters. Ignoring request: {line}")
                        continue
                    request = f" P {key} {value}"
                    send_request(client_socket, request)

        client_socket.close()
    except Exception as e:
        print(f"Error: {e}")
    
    
    
                    
                    
        
       
                    
  
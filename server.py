import socket
import threading

clients = []  # List to store client sockets
client_names = {}  # Dictionary to store client names
client_count = 0  # Counter to assign unique names to clients

def handle_client(client_socket, client_name):
    try:
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if message:
                    if message.strip().upper() == "CLOSE SOCKET":
                        print(f"Client {client_name} requested to close the connection.")
                        break

                    formatted_message = f"{client_name}: {message}"
                    print(formatted_message)
                    # Respond to the client with the same message in uppercase
                    response = message.upper()
                    client_socket.sendall(response.encode('utf-8'))
                else:
                    print(f"Client {client_name} disconnected.")
                    break
            except Exception as e:
                print(f"Error receiving message from {client_name}: {e}")
                break
    finally:
        client_socket.close()
        if client_socket in clients:
            clients.remove(client_socket)
        if client_socket in client_names:
            del client_names[client_socket]
        print(f"Client {client_name} removed. Current clients: {len(clients)}")

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.sendall(message.encode('utf-8'))
            except Exception as e:
                print(f"Error broadcasting to {client_names.get(client, 'unknown client')}: {e}")
                client.close()
                if client in clients:
                    clients.remove(client)
                if client in client_names:
                    del client_names[client]

def send_messages():
    while True:
        message = input()
        formatted_message = f"Server: {message}"
        print(formatted_message)  # Print server messages locally
        broadcast(formatted_message, None)

def start_server():
    global client_count

    host = 'localhost'  # Listen on all interfaces (can be changed to a fixed IP for operating on different devices)
    port = 56040  # Can be adjusted to any usable port

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Server listening on {host}:{port}")

        while True:
            try:
                print("Waiting for a new connection...")
                client_socket, client_address = server_socket.accept()
                print(f"Accepted connection from {client_address}")
                client_count += 1
                client_name = f"Client {client_count}"
                print(f"Assigning name {client_name} to the connection")
                clients.append(client_socket)
                client_names[client_socket] = client_name

                client_handler = threading.Thread(target=handle_client, args=(client_socket, client_name))
                client_handler.start()
            except Exception as e:
                print(f"Error accepting connection: {e}")
    except PermissionError as e:
        print(f"PermissionError: {e}")
        print("Ensure you have the necessary permissions or try using a different port.")
    except OSError as e:
        print(f"OS error: {e}")
        print("Ensure the port is available and not in use by another application.")
    except Exception as e:
        print(f"Server error: {e}")
    finally:
        server_socket.close()

if __name__ == '__main__':
    send_thread = threading.Thread(target=send_messages)
    send_thread.daemon = True  # Ensure send_thread exits when the main thread does
    send_thread.start()
    start_server()

import socket
import threading

def handle_server(server_socket):
    while True:
        try:
            message = server_socket.recv(1024).decode('utf-8')
            if message:
                print(message)  # Print the message from the server (in uppercase)
            else:
                print("Server closed the connection.")
                break
        except Exception as e:
            print(f"Error receiving message from server: {e}")
            break
    server_socket.close()

def send_messages(server_socket):
    while True:
        try:
            message = input()
            if message.strip().upper() == "CLOSE SOCKET":  # If the message is "CLOSE SOCKET", close the connection
                server_socket.sendall(message.encode('utf-8'))
                print("Closing connection to the server...")
                break  # Break the loop to terminate the connection
            server_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            print(f"Error sending message to server: {e}")
            break

def start_client():
    server_ip = input("Enter the server IP address: ")
    # To operate on a localhost:
    # simply type localhost or type this IP 127.0.0.1

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    while True:
        command = input("Type 'CONNECT' to connect to the server: ")
        if command.strip().upper() == 'CONNECT':
            try:
                port = 56040  # Define the port variable
                print(f"Attempting to connect to {server_ip}:{port}")
                server_socket.connect((server_ip, port))
                print("Connected to the server")

                # Start a thread to handle incoming messages from the server
                server_handler = threading.Thread(target=handle_server, args=(server_socket,))
                server_handler.start()

                # Handle sending messages to the server
                send_messages(server_socket)
            except Exception as e:
                print(f"Connection error: {e}")
            finally:
                server_socket.close()
                print("Disconnected from the server")
            break
        else:
            print("Invalid command. Please type 'CONNECT' to proceed.")

if __name__ == '__main__':
    start_client()

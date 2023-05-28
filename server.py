import socket
import threading

def handle_client(client_socket):
    client_socket.send(b'Welcome Sir')

    while True:
        message = client_socket.recv(1024).decode()

        if message == 'FIN':
            client_socket.send(b'BYE')
            break

        if message.startswith('CALC'):
            _, a, b, operator = message.split()

            result = None
            if operator == '+':
                result = int(a) + int(b)
            elif operator == '-':
                result = int(a) - int(b)
            elif operator == '*':
                result = int(a) * int(b)
            elif operator == '/':
                try:
                    result = int(a) / int(b)
                except ZeroDivisionError:
                    result = 'Error: Division by Zero'

            client_socket.sendall(f'Ur result : {result}'.encode())

    client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8888))
    server_socket.listen(5)
    print('Server listening on port 8888...')

    while True:
        client_socket, address = server_socket.accept()
        print(f'Connected to {address}')

        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

start_server()

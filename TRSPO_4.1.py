import socket

HOST = "127.0.0.1"  # Локальний сервер
PORT = 65433        # Той самий порт, що й у сервера

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))  # Підключення до сервера
    print("Підключено до сервера.")
    client_socket.sendall("Привіт, сервер!".encode())  # Надсилаємо повідомлення
    data = client_socket.recv(1024)           # Чекаємо відповіді
    print(f"Отримано від сервера: {data.decode('utf-8')}")

import socket

HOST = '127.0.0.1'
PORT = 65433

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))  # Прив'язка до IP та порту
    server_socket.listen()
    print(f"Сервер запущено на {HOST}:{PORT}, очікуємо підключень...")

    conn, addr = server_socket.accept()  # Очікуємо на підключення
    with conn:
        print(f"Клієнт підключився: {addr}")
        data = conn.recv(1024)  # Отримуємо дані від клієнта
        if data:
            print(f"Отримано: {data.decode()}")
            conn.sendall("Прийнято!".encode())  # Відправляємо байти

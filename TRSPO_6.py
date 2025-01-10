import socket
import struct

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 12345))
    server_socket.listen(1)
    print("Сервер запущено, очікування підключення...")
    conn, addr = server_socket.accept()
    print(f"Підключено до клієнта: {addr}")

    for _ in range(100):
        # Приймаємо заголовок (довжина повідомлення)
        header = conn.recv(4)
        if not header:
            break
        msg_length = struct.unpack('!I', header)[0]  # Розпаковуємо довжину
        # Приймаємо основне повідомлення
        msg_data = conn.recv(msg_length)
        msg_type, = struct.unpack('!B', msg_data[:1])  # Тип повідомлення
        if msg_type == 1:  # Текст
            message = msg_data[1:].decode('utf-8')
            print(f"Отримано текстове повідомлення: {message}")
        elif msg_type == 2:  # Ціле число
            number = struct.unpack('!i', msg_data[1:])[0]
            print(f"Отримано ціле число: {number}")
        elif msg_type == 3:  # Дійсне число
            number = struct.unpack('!f', msg_data[1:])[0]
            print(f"Отримано дійсне число: {number}")

    conn.close()
    server_socket.close()

if __name__ == "__main__":
    server()

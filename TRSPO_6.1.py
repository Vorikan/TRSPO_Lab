import socket
import struct

def client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 12345))

    # Відправляємо 100 повідомлень різних типів
    for i in range(1, 101):
        if i % 3 == 1:
            # Текстове повідомлення
            msg_type = 1
            message = f"Повідомлення {i}"
            msg_data = struct.pack('!B', msg_type) + message.encode('utf-8')
        elif i % 3 == 2:
            # Ціле число
            msg_type = 2
            number = i
            msg_data = struct.pack('!B', msg_type) + struct.pack('!i', number)
        else:
            # Дійсне число
            msg_type = 3
            number = i * 1.1
            msg_data = struct.pack('!B', msg_type) + struct.pack('!f', number)

        # Створюємо заголовок (довжина повідомлення)
        header = struct.pack('!I', len(msg_data))
        # Відправляємо заголовок і повідомлення
        client_socket.sendall(header + msg_data)

    client_socket.close()

if __name__ == "__main__":
    client()

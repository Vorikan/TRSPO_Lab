import socket

def start_client():
    # Створюємо TCP сокет
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Підключаємося до сервера
    client_socket.connect(('localhost', 12345))
    
    while True:
        # Вводимо повідомлення для відправки
        message = input("Ваше повідомлення: ")
        client_socket.send(message.encode())
        
        # Отримуємо відповідь від сервера
        response = client_socket.recv(1024).decode()
        print(f"Сервер: {response}")
        
        if message.lower() == 'exit':
            break
    
    # Закриваємо сокет
    client_socket.close()

if __name__ == "__main__":
    start_client()
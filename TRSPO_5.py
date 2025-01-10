import socket

def start_server():
    # Створюємо TCP сокет
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Прив'язуємо сокет до адреси та порту
    server_socket.bind(('localhost', 12345))
    
    # Слухаємо вхідні з'єднання
    server_socket.listen(1)
    print("Сервер запущено, чекаємо на з'єднання...")
    
    # Приймаємо з'єднання
    client_socket, addr = server_socket.accept()
    print(f"З'єднано з {addr}")
    
    while True:
        # Отримуємо дані від клієнта
        data = client_socket.recv(1024).decode()
        if not data:
            break
        print(f"Клієнт: {data}")
        
        # Відправляємо відповідь клієнту
        response = input("Ваша відповідь: ")
        client_socket.send(response.encode())
    
    # Закриваємо сокети
    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    start_server()
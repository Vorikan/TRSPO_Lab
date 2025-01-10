import socket
import numpy as np
from concurrent.futures import ThreadPoolExecutor


# Функція для обчислення множення матриць
def multiply_matrices(matrix_a, matrix_b):
    try:
        return np.dot(matrix_a, matrix_b)
    except ValueError as e:
        print("Помилка при множенні матриць:", e)
        return None


# Функція для обробки клієнта
def handle_client(client_socket):
    try:
        # Отримуємо розміри матриць
        dims_data = client_socket.recv(1024).decode("utf-8")
        N, M, L = map(int, dims_data.split())
        print(f"Отримано розміри матриць: N={N}, M={M}, L={L}")

        # Отримуємо матриці (дані можуть бути розподілені на кілька частин)
        total_bytes = N * M * 4  # Число байт для матриці A
        matrix_a_data = b""
        while len(matrix_a_data) < total_bytes:
            matrix_a_data += client_socket.recv(total_bytes - len(matrix_a_data))

        total_bytes = M * L * 4  # Число байт для матриці B
        matrix_b_data = b""
        while len(matrix_b_data) < total_bytes:
            matrix_b_data += client_socket.recv(total_bytes - len(matrix_b_data))

        # Перетворення отриманих байтів у матриці
        matrix_a = np.frombuffer(matrix_a_data, dtype=np.float32).reshape(N, M)
        matrix_b = np.frombuffer(matrix_b_data, dtype=np.float32).reshape(M, L)

        print("Матриці отримано. Виконуються обчислення...")

        # Перевірка на відповідність розмірів для множення
        if matrix_a.shape[1] != matrix_b.shape[0]:
            print("Помилка: Несумісні розміри матриць для множення!")
            client_socket.send("Помилка: Несумісні розміри матриць!".encode())
            return

        # Обчислення результату множення матриць
        result_matrix = multiply_matrices(matrix_a, matrix_b)

        if result_matrix is not None:
            # Відправка результату клієнту
            result_data = result_matrix.astype(np.float32).tobytes()
            client_socket.send(result_data)
            print("Результат надіслано клієнту.")
        else:
            client_socket.send("Помилка при обчисленні.".encode())
    except Exception as e:
        print(f"Помилка при обробці запиту клієнта: {e}")
    finally:
        client_socket.close()


def start_server(host='127.0.0.1', port=12345):
    # Створення сокету
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Сервер запущено на {host}:{port}. Очікування підключень...")

    with ThreadPoolExecutor() as executor:
        while True:
            # Прийом клієнтського з'єднання
            client_socket, client_address = server.accept()
            print(f"Підключено клієнта: {client_address}")
            # Обробка клієнта в окремому потоці
            executor.submit(handle_client, client_socket)


if __name__ == '__main__':
    start_server()

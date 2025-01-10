import socket
import numpy as np

def generate_matrices():
    # Генерація випадкових розмірів матриць
    N = np.random.randint(1000, 2000)
    M = np.random.randint(1000, 2000)
    L = np.random.randint(1000, 2000)

    # Генерація випадкових матриць
    matrix_a = np.random.rand(N, M).astype(np.float32)
    matrix_b = np.random.rand(M, L).astype(np.float32)

    return matrix_a, matrix_b, N, M, L


def send_matrices_to_server(matrix_a, matrix_b, N, M, L, host='127.0.0.1', port=12345):
    try:
        # Встановлення з'єднання з сервером
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))

        # Відправлення розмірів матриць
        dims_data = f"{N} {M} {L}"
        client.send(dims_data.encode())

        # Відправлення матриць
        client.send(matrix_a.tobytes())
        client.send(matrix_b.tobytes())

        # Отримання результату від сервера
        result_data = b""
        expected_size = N * L * 4  # Очікуваний розмір результату
        while len(result_data) < expected_size:
            result_data += client.recv(expected_size - len(result_data))

        # Перевірка розміру отриманих даних
        if len(result_data) != expected_size:
            print(f"Помилка: отримано {len(result_data)} байт, очікувалося {expected_size} байт.")
            return

        # Перетворення результату в матрицю
        result_matrix = np.frombuffer(result_data, dtype=np.float32).reshape(N, L)

        print(f"Розміри матриць: N={N}, M={M}, L={L}")
        print("Матриці згенеровано.")
        print("Розрахований результат:")
        print(result_matrix)

    except Exception as e:
        print(f"Помилка при підключенні до сервера: {e}")
    finally:
        client.close()


if __name__ == '__main__':
    # Генерація матриць
    matrix_a, matrix_b, N, M, L = generate_matrices()
    
    # Підключення до сервера та відправлення матриць
    send_matrices_to_server(matrix_a, matrix_b, N, M, L)

from multiprocessing.pool import ThreadPool
from threading import Lock
from time import time

def collatz_steps(n):
    """Обчислення кількості кроків за гіпотезою Колаца для числа n."""
    steps = 0
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        steps += 1
    return steps

def process_numbers(numbers, lock, total_steps, count):
    """Обробка чисел і оновлення загальної кількості кроків та рахунку."""
    for num in numbers:
        steps = collatz_steps(num)
        with lock:
            total_steps[0] += steps
            count[0] += 1

def main():
    # Генерація чисел
    total_numbers = 10_000_000
    num_threads = 8  # Задати кількість потоків вручну
    numbers = range(1, total_numbers + 1)
    
    # Спільні змінні
    total_steps = [0]  # Використовуємо список для мутабельності
    count = [0]
    lock = Lock()
    
    # Розподіл чисел на частини
    chunk_size = total_numbers // num_threads
    chunks = [numbers[i:i + chunk_size] for i in range(0, total_numbers, chunk_size)]
    
    # Паралельна обробка
    start_time = time()
    with ThreadPool(num_threads) as pool:
        pool.starmap(process_numbers, [(chunk, lock, total_steps, count) for chunk in chunks])
    
    # Середнє значення
    average_steps = total_steps[0] / count[0]
    end_time = time()
    
    print(f"Середня кількість кроків: {average_steps:.2f}")
    print(f"Час виконання: {end_time - start_time:.2f} секунд")

if __name__ == "__main__":
    main()

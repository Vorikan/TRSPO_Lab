import threading
import time

def calculate_square(numbers):
    for n in numbers:
        time.sleep(1)
        print(f'Square: {n*n}')

def calculate_cube(numbers):
    for n in numbers:
        time.sleep(1)
        print(f'Cube: {n*n*n}')

numbers = [1, 2, 3, 4]
t1 = threading.Thread(target=calculate_square, args=(numbers,))
t2 = threading.Thread(target=calculate_cube, args=(numbers,))

t1.start()
t2.start()

t1.join()
t2.join()

print("Done!")
print("Hello, world! It's rainy today")

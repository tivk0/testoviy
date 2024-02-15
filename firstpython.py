# Функция, которая генерирует матрицу 5×5 и заполняет её случайными значениями и возвращает минимальное и максимальное значения полученной матрицы.
import numpy as np

def generate_random_matrix():
    matrix = np.random.randint(1, 1000, size=(5, 5))
    print(matrix)
    min_value = np.min(matrix)
    max_value = np.max(matrix)
    return min_value, max_value

min_val, max_val = generate_random_matrix()
print(f"Мин значение: {min_val}")
print(f"Макс значение: {max_val}")

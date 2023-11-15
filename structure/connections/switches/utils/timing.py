import time


# декоратор для проверки скорости методов
def timing(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Метод '{func.__name__}' --- {execution_time:.2f} сек")
        # if func.__name__ != 'read' and func.__name__ != '_find':
        #     print(' ')
        return result
    return wrapper

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


# ставит склонение слова "день" в зависимости от кол-ва дней
def plural_days(n):
    days = ['день', 'дня', 'дней']

    if n % 10 == 1 and n % 100 != 11:
        return days[0]
    elif 2 <= n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20):
        return days[1]
    else:
        return days[2]
import time


def speed_calc_decorator(func):
    def wrapper_func():
        start_time = time.time()
        func()
        end_time = time.time()
        print(f'{func.__name__} run speed: {end_time - start_time}')
    return wrapper_func


@speed_calc_decorator
def fast_function():
    for i in range(1000000):
        i * i


@speed_calc_decorator
def slow_function():
    for i in range(10000000):
        i * i


if __name__ == '__main__':
    fast_function()
    slow_function()
def logging_decorator(function):
    def wrapper_func(*args):
        print(f'You called {function.__name__}{args}')
        result = function(*args)
        print(f'It returned: {result}')
        return result

    return wrapper_func


@logging_decorator
def a_function(*args):
    return sum(args)


a_function(1, 2, 3)
def log_f_name(function):
    def wrapper_func():
        """
        prints then executes the provided function
        """
        print(f'Executing {function.__name__}')
        function()
        print('Execution complete')
    return wrapper_func


@log_f_name
def greet():
    print('Hello')

@log_f_name
def farewell():
    print('Good-bye!!')

@log_f_name
def enquire_stat():
    print('How are you?')


farewell()
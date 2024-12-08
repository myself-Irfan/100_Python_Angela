class User:
    def __init__(self, name: str):
        self.name = name
        self.is_logged_in = False

# function as param since decorator func will wrap it
def is_auth_decorator(function):
    # since inputted function may have args & kwargs
    def wrapper_func(*args, **kwargs):
        # first arg's(User) property
        if args[0].is_logged_in:
            return function(args[0])
    return wrapper_func


@is_auth_decorator
def show_post(user: User) -> str:
    return f"This is {user.name}'s post"


if __name__ == '__main__':
    usr_irfan = User('irfan')
    # not logged in
    print(show_post(usr_irfan))

    # logged in
    usr_irfan.is_logged_in = True
    print(show_post(usr_irfan))
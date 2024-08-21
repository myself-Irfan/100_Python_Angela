class User:
    def __init__(self, name: str = 'John Doe'):
        """
        inits class obj with provided input or default str
        :param name: string
        """
        self._name = name
        print('Initialising a new obj of User class')

    def get_name(self) -> str:
        """
        :return: class attribute name
        """
        return self._name

    def set_name(self, name: str):
        """
        updates an obj's attribute name
        :param name: string
        """
        self._name = name

    def greet(self) -> None:
        """
        prints obj attrib name
        :return: None
        """
        print(f'Salutation from {self._name}')


if __name__ == '__main__':
    u1 = User()

    u2 = User()
    u2.set_name('Yen')

    u3 = User('Irfan')

    u1.greet()
    u2.greet()
    u3.greet()
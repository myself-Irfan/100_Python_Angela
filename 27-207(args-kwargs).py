"""
This script demonstrates unlimited args & keyword args
"""

class SampleCls:
    def __init__(self, **kwargs):
        """
        default value if no kwarg not provided
        """
        self.name = kwargs.get('name', 'John Doe')
        self.age = kwargs.get('age', 18)

    def introduce_self(self):
        print(f'Hello! I am {self.name} and of {self.age}')


def return_plus(*args: int) -> int:
    print(type(args))
    sum_value = 0
    for num in args:
        sum_value += num
    return sum_value


def calculate(init_num: int, **kwargs):
    print(kwargs)
    init_num += kwargs['add']
    print(init_num)
    init_num *= kwargs['multiply']
    print(init_num)


if __name__ == '__main__':
    print(return_plus(1, 2, 3, 4, 5))
    calculate(5, add=2, multiply=3)

    irfan = SampleCls(name='Irfan', age=28)
    who_knows = SampleCls()

    irfan.introduce_self()
    who_knows.introduce_self()
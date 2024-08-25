# this script demonstrates a simple instance of class inheritance

class Animal:
    def __init__(self, name: str):
        self.eyes = 2
        self.name = name

    def greet(self):
        print(f'I am {self.name} of {__class__.__name__} class')


class Fish(Animal):
    def __init__(self, name: str):
        super().__init__(name)

    def greet(self):
        super().greet()
        print(f'Living underwater in {__class__.__name__} class')


if __name__ == '__main__':
    i_beast = Animal('Black Beast')
    i_beast.greet()
    print()
    i_fish = Fish('Leviathan')
    i_fish.greet()

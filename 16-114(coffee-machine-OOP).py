import logging


class Loggable:
    def log(self, level: int, message: str):
        logger.log(level, f'{self.__class__.__name__}: {message}')


class MenuItem(Loggable):
    def __init__(self, name: str, water: int, milk: int, coffee: int, cost: float):
        self._name = name
        self._cost = cost
        self._ingredients = {
            "water": water,
            "milk": milk,
            "coffee": coffee
        }

    @property
    def name(self):
        return self._name

    @property
    def cost(self):
        return self._cost

    @property
    def ingredients(self):
        return self._ingredients


class Menu(Loggable):
    def __init__(self):
        self._menu = [
            MenuItem(name="latte", water=200, milk=150, coffee=24, cost=2.5),
            MenuItem(name="espresso", water=50, milk=0, coffee=18, cost=1.5),
            MenuItem(name="cappuccino", water=250, milk=50, coffee=24, cost=3)
        ]

    def get_items(self) -> list[str]:
        return [item.name for item in self._menu]

    def find_drink(self, order_name: str) -> MenuItem | None:
        for item in self._menu:
            if item.name == order_name:
                return item
        self.log(logging.ERROR, f'{order_name} not in the menu')
        return None


class CoffeeMaker(Loggable):
    def __init__(self):
        self._resources = {
            'water': 300,
            'milk': 200,
            'coffee': 100
        }

    def report(self) -> None:
        self.log(logging.INFO, 'Reporting current resources')
        print(f'Current resource:\nWater: {self._resources["water"]}ml\nMilk: {self._resources["milk"]}ml\nCoffee: {self._resources["coffee"]}g')

    def is_resource_sufficient(self, drink: MenuItem) -> bool:
        for item in drink.ingredients:
            if drink.ingredients[item] > self._resources[item]:
                self.log(logging.WARNING, 'Resources insufficient')
                print(f'{item} not sufficient in resources')
                return False
        return True

    def make_coffee(self, drink: MenuItem) -> None:
        for item in drink.ingredients:
            self._resources[item] -= drink.ingredients[item]
        self.log(logging.INFO, 'coffee procured')
        print(f'Enjoy your {drink.name}')


class MoneyMachine(Loggable):
    CURRENCY = "৳"

def main():
    pass


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    main()

import logging


class Loggable:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def log(self, level: int, message: str):
        self.logger.log(level, message)


class MenuItem(Loggable):
    def __init__(self, name: str, water: int, milk: int, coffee: int, cost: float):
        super().__init__()
        self._name = name
        self._cost = cost
        self._ingredients = {
            "water": water,
            "milk": milk,
            "coffee": coffee
        }

    # def to access attribute outside class as property
    @property
    def name(self) -> str:
        return self._name

    @property
    def cost(self) -> float:
        return self._cost

    @property
    def ingredients(self) -> dict[str, int]:
        return self._ingredients


class Menu(Loggable):
    def __init__(self):
        super().__init__()
        self._menu = [
            MenuItem(name="latte", water=200, milk=150, coffee=24, cost=250),
            MenuItem(name="espresso", water=50, milk=0, coffee=18, cost=150),
            MenuItem(name="cappuccino", water=250, milk=50, coffee=24, cost=300)
        ]

    def get_items(self) -> list[str]:
        """
        returns a list of items in Menu class menu property
        :return: list of string
        """
        self.log(logging.INFO, 'Returning items from Menu class property _menu')
        return [item.name for item in self._menu]

    def find_drink(self, order_name: str) -> MenuItem | None:
        """
        takes a string and compares with Menu class items then
        returns the corresponding item else None
        :param order_name: str
        :return: an obj of MenuItem class or None
        """
        self.log(logging.INFO, f'Comparing received {order_name} with items in _menu')
        for item in self._menu:
            if item.name == order_name or item.name.startswith(order_name):
                return item
        return None


class CoffeeMaker(Loggable):
    def __init__(self):
        super().__init__()
        self._resources = {
            'water': 300,
            'milk': 200,
            'coffee': 100
        }

    def report(self) -> None:
        """
        prints values of attributes
        :return: None
        """
        self.log(logging.INFO, 'Printing current resources')
        print(
            f'Current resources:\nWater: {self._resources["water"]}ml\nMilk: {self._resources["milk"]}ml\nCoffee: {self._resources["coffee"]}g'
        )

    def is_resource_sufficient(self, drink: MenuItem) -> bool:
        """
        compares input obj attributes with resources and if resource item is more than resource
        then returns True else False
        :param drink: Menu item obj
        :return: bool
        """
        for item in drink.ingredients:
            if drink.ingredients[item] > self._resources[item]:
                self.log(logging.WARNING, 'Resources insufficient')
                print(f'{item} not enough to prepare {drink.name}')
                return False
        return True

    def make_coffee(self, drink: MenuItem) -> None:
        """
        subtracts the item's value from resource for each ingredient
        :param drink: Menu item obj
        :return: None
        """
        for item in drink.ingredients:
            self._resources[item] -= drink.ingredients[item]
        self.log(logging.INFO, 'Resources updated')
        print(f'Enjoy your {drink.name}')


class MoneyMachine(Loggable):
    CURRENCY = "৳"
    COIN_VALUES = {
        'hundred': 100,
        'fifty': 50,
        'twenty': 20,
        'ten': 10
    }

    def __init__(self):
        super().__init__()
        self._profit = 0
        self._money_received = 0

    def report(self) -> None:
        """
        prints current profit
        :return: None
        """
        self.log(logging.INFO, 'Printing current profit')
        print(f'Current profit: {self.CURRENCY}{self._profit}')

    def process_coins(self, cost: float) -> float:
        """
        takes count of bills from user, calculates amount and sums then returns the total_amt
        :param cost: float
        :return: float
        """
        self.log(logging.INFO, 'Taking input for money')
        for bill, value in self.COIN_VALUES.items():
            if self._money_received >= cost:
                break
            self._money_received += int(input(f'How many {self.CURRENCY}{bill}?')) * value

        return self._money_received

    def make_payment(self, cost: float) -> bool:
        """
        takes cost, updates attributes and
        returns True for successful payment or False for failure
        :param cost: float
        :return: bool
        """
        print(f'Your bill is {self.CURRENCY}{cost}')
        payment = self.process_coins(cost)
        if payment >= cost:
            self.log(logging.INFO, 'Payment successful')
            change = round(payment - cost, 2)
            self._profit += cost
            self._money_received = 0
            print(f"Here is {self.CURRENCY}{change} in change.")
            return True
        else:
            self.log(logging.WARNING, 'Payment failed')
            print(f'Insufficient funds. {self.CURRENCY}{payment} refunded')
            self._money_received = 0
            return False


def main():
    coffee_maker = CoffeeMaker()
    money_machine = MoneyMachine()
    menu = Menu()

    while True:
        options = menu.get_items()
        choice = input(f'What would you like? ({", ".join(options)}) ').strip().lower()

        if choice == 'q':
            break
        elif choice == 'r':
            coffee_maker.report()
            money_machine.report()
        else:
            drink = menu.find_drink(choice)
            if drink:
                if drink and coffee_maker.is_resource_sufficient(drink) and money_machine.make_payment(drink.cost):
                    coffee_maker.make_coffee(drink)
                else:
                    print('Unable to prepare your drink.')
            else:
                print('Please choose an item from the menu')

        while True:
            nxt_itr = input('Do you want to continue? (yes/no) ').strip().lower()

            if nxt_itr in ('y', 'yes'):
                break
            elif nxt_itr in ('n', 'no'):
                print('Thank you for using iCoffeeMachine. Till next time')
                return
            else:
                print('Please provide proper input')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()

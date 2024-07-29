def get_usr_c() -> str:
    while True:
        usr_c = input('Enter your choice\n"E" for espresso\n"L" for latte\n"C" for cappuccino\n').lower()
        if usr_c == 'q':
            exit()
        elif usr_c == 'r':
            print_report()
        elif usr_c in ['e', 'l', 'c']:
            return usr_c
        else:
            print('Please provide accurate info')


def print_report():
    print(
        f'Current resource:\nWater: {resources.get('water')}ml\nMilk: {resources.get('milk')}ml\nCoffee: {resources.get('coffee')}g\nMoney: ${money}')


def check_resources(choice_ing: dict) -> bool:
    for ing in choice_ing:
        if resources[ing] < choice_ing[ing]:
            print(f'{ing} not available')
            return False
    return True


<<<<<<< HEAD
def take_coin(cost: int) -> tuple[bool, int]:
    total = 0
    while total != cost:
        pass


=======
>>>>>>> 9c13fa6f2019a85d46199b03b41b08683b6b2114
def make_drink():
    pass


def main():
    usr_c = get_usr_c()
    usr_c = MENU[usr_c]

    print(f'You want {usr_c}')

    is_available = check_resources(MENU_ING.get(usr_c).get('ingredients'))

    if is_available:
        print(f'Can make {usr_c}')
    else:
        print(f'Can not make {usr_c}')


if __name__ == '__main__':
    MENU_ING = {
        "espresso": {
            "ingredients": { "water": 50, "coffee": 18 },
            "cost": 1.5,
        },
        "latte": {
            "ingredients": { "water": 200, "milk": 150, "coffee": 24 },
            "cost": 2.5,
        },
        "cappuccino": {
            "ingredients": { "water": 250, "milk": 100, "coffee": 24 },
            "cost": 3.0,
        }
    }

    MENU = {
        'e': 'espresso',
        'l': 'latte',
        'c': 'cappuccino'
    }

    resources = {
        'water': 1000,
        'milk': 700,
        'coffee': 500
    }

    money = 0

    main()

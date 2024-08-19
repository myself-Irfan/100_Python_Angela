def get_usr_c() -> str:
    while True:
        usr_c = input('Enter your choice\n"E" for espresso\n"L" for latte\n"C" for cappuccino\n').lower()
        if usr_c == 'q':
            exit()
        elif usr_c == 'r':
            print_report()
        elif usr_c in MENU:
            return usr_c
        else:
            print('Please provide accurate info')


def print_report():
    print(
        f'Current resource:\nWater: {resources.get("water")}ml\nMilk: {resources.get("milk")}ml\nCoffee: {resources.get("coffee")}g\nMoney: ${money}')


def check_resources(choice_ing: dict) -> bool:
    for ing, amt_req in choice_ing.items():
        if resources[ing] < amt_req:
            print(f'Warning! {ing} not sufficient')
            return False
    return True


def take_coin(cost: float) -> float:
    print(f'Total bill is ${cost}. Please insert coins')
    total = 0

    for key, value in COIN_T.items():
        while True:
            try:
                amt = int(input(f'How many {key}? '))
                total += amt * value
                break
            except ValueError:
                print("Please enter a valid number")

    if total >= cost:
        change = total - cost
        return change
    else:
        print(f"Not enough coins. Refunding coins. Missing amount ${cost-total}")
        return -1


def make_drink(choice_ing):
    for ing, req_amt in choice_ing.items():
        resources[ing] -= req_amt

    print('Enjoy your drink')


def main():
    global money
    usr_c = get_usr_c()
    usr_c = MENU[usr_c]

    print(f'You want {usr_c}')

    is_available = check_resources(MENU_ING.get(usr_c).get('ingredients'))

    if is_available:
        print(f'Can make {usr_c}')
        change = take_coin(MENU_ING.get(usr_c).get('cost'))
        if change != -1:
            money += MENU_ING.get(usr_c).get('cost')  # Update global money with the cost
            make_drink(MENU_ING.get(usr_c).get('ingredients'))
            if change > 0:
                print(f'Take change {change}')
        else:
            print('Transaction failed')
    else:
        print(f'Can not make {usr_c}')

    return input("Continue? (Y/N)").strip().lower()


if __name__ == '__main__':
    MENU_ING = {
        "espresso": {
            "ingredients": {"water": 50, "coffee": 18},
            "cost": 1.5,
        },
        "latte": {
            "ingredients": {"water": 200, "milk": 150, "coffee": 24},
            "cost": 2.5,
        },
        "cappuccino": {
            "ingredients": {"water": 250, "milk": 100, "coffee": 24},
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

    COIN_T = {
        "quarters": 0.25,
        "dimes": 0.10,
        "pennies": 0.01
    }

    while True:
        res = main()
        if res == 'n':
            print('Terminating...')
            break
        elif res == 'y':
            continue
        elif res == 'r':
            print_report()
        else:
            print("Please provide valid input ('y' to continue or 'n' to terminate)")

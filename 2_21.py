while True:
    usr_in = input('Enter only digits: ')
    if usr_in.isdigit():
        break
    else:
        print('Only give numbers')

x = 0

for _ in usr_in:
    x += int(_)

print(f'Sum of {usr_in} is {x}')
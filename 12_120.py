# global fun manipulation
health = 10


def drink_potion():
    global health
    health += 2


def drink_potion2():
    return health + 1


print(health)
drink_potion()
print(health)
drink_potion2()
print(health)


import random
import string

wrd_li = string.ascii_lowercase

travel_log = [
    {
        'name': 'Irfan',
        'score': 100,
        'languages': ['Python', 'Django', 'DRF', 'React']
    },
    {
        'name': 'Afzal',
        'score': 80,
        'languages': ['Python', 'Django']
    }
]


def gen_rand_wrd() -> str:
    k = random.randint(3, 6)
    return ''.join(random.choices(wrd_li, k=k))


def gen_rand_int() -> int:
    return random.randint(1, 100)


def add_dict():
    l = [gen_rand_wrd() for _ in range(5)]

    new_entry = {
        'name': gen_rand_wrd(),
        'score': gen_rand_int(),
        'languages': l
    }

    # entry checks if name exists, next checks if entry exists then return entry else None as specified
    existent_ent = next((entry for entry in travel_log if entry['name'] == new_entry['name']), None)

    if existent_ent:
        # instead of update(), selective update
        existent_ent['score']: gen_rand_int()
        # extending the list for already existent
        existent_ent['languages'].extend(new_entry['languages'])
    else:
        travel_log.append(new_entry)


if __name__ == '__main__':
    print(travel_log)

    add_dict()

    print(travel_log)



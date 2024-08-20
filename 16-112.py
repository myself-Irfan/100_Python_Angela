from prettytable import PrettyTable


def format_data(data: dict[str, list[str]]) -> dict[str, list[str]]:
    return {
        key.upper(): [value.capitalize() for value in values]
        for key, values in data.items()
    }


def dict_2_table(data: dict[str, list[str]]):
    table = PrettyTable()
    table.field_names = list(data.keys())
    rows = zip(*data.values())
    for row in rows:
        table.add_row(row)

    table.align = "l"

    return table


if __name__ == '__main__':
    data_d = {
        'name': ['moltres', 'zapdos', 'articuno'],
        'type': ['fire', 'lightning', 'ice']
    }

    form_d = format_data(data_d)

    pk_table = dict_2_table(form_d)
    print(pk_table)

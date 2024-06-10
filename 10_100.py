def get_title_name(name: str) -> str:
    if not name:
        raise ValueError('Can not be empty')
    return name.title()


if __name__ == '__main__':
    try:
        print(get_title_name(''))
    except ValueError as e:
        print(e)

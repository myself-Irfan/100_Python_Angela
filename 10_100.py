def get_title_name(name: str) -> str:
    '''
    returns a title case of the provided str, for empty in raises ValueError
    :param name: str
    :return: str
    '''

    if not name:
        raise ValueError('Can not be empty')
    return name.title()


if __name__ == '__main__':
    try:
        print(get_title_name(''))
    except ValueError as e:
        print(e)

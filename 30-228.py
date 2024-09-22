def div_num(a: int, b: int) -> int | None:
    try:
        a = int(a)
        b = int(b)
        result = a//b
    except ZeroDivisionError as z_error:
        print(f'Input needs to be greater than 0 | {z_error}')
        result = None
    except ValueError as v_error:
        print(f'Input need to be number | {v_error}')
        result = None
    except TypeError as t_error:
        print(f'Input needs to be int | {t_error}')
        result = None
    else:
        print(f'Result is {result}')
    finally:
        print(f'Execution complete for {a}/{b}')
        return result


def get_bmi(height: float, weight: int) -> int:
    if height > 3:
        raise ValueError('Human size can not be greater than 3 meters')

    return int(weight / pow(height, 2))


if __name__ == '__main__':
    print(div_num(3, 0))
    print(div_num('3a',1))
    print(div_num(None,3))

    # print(get_bmi(4, 30))
    print(get_bmi(3, 30))
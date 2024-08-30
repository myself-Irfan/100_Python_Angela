from pandas import read_csv


def c2f(temp: int) -> float:
    temp_f = (temp * 9 / 5) + 32
    return round(temp_f, 2)


def main() -> None:
    in_data = read_csv(F_NAME)
    print(in_data.shape)

    temp_li = in_data.get('temp')
    temp_li.to_list()

    avg_tmp = round(temp_li.mean(), 2)
    print(f'Avg: {avg_tmp}\tMax: {temp_li.max()}')

    # row specific
    print(in_data[in_data.get('temp') == temp_li.max()])

    in_data['temp'] = in_data.get('temp').apply(c2f)
    print(in_data)

    in_data.to_csv(F_NAME)


if __name__ == '__main__':
    F_NAME = '25-190.csv'

    main()

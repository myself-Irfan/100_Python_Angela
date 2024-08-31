from pandas import read_csv


def main():
    f_df = read_csv('26-201.csv')
    f_dict = dict(zip(f_df.letter, f_df.code))

    usr_in = input('Giv your name').upper()
    print(usr_in)

    name_str = {c : f_dict[c] for c in usr_in if c != ' '}
    print(name_str)


if __name__ == '__main__':
    main()
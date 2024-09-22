from pandas import read_csv


def validate_usr_in() -> str:
    while True:
        usr_in = input('Enter your name: ').upper()
        if usr_in.replace(' ', '').isalpha():
            return usr_in
        else:
            print('Input must contain only letters and spaces')

def main():
    f_df = read_csv('26-201.csv')
    f_dict = dict(zip(f_df.letter, f_df.code))

    usr_in = validate_usr_in()
    print(usr_in)

    name_str = {c : f_dict[c] for c in usr_in if c != ' '}
    print(name_str)


if __name__ == '__main__':
    main()
import random
import string

alpha_li = list(string.ascii_lowercase)
num_li = list(string.digits)
sp_char = list(string.punctuation)


def get_usr_in() -> tuple:
    wrd_len = random.randint(1, 10)
    sym_len = random.randint(1, 3)
    num_len = random.randint(1, 3)

    return wrd_len, sym_len, num_len


def gen_pwd(wrd_len:int, sym_len:int, num_len:int) -> str:
    pwd_wrd = []
    for _ in range(wrd_len + 1):
        pwd_wrd.append(random.choice(alpha_li))

    pwd_num = []
    for _ in range(num_len + 1):
        pwd_num.append(random.choice(num_li))

    pwd_sym = []
    for _ in range(sym_len + 1):
        pwd_sym.append(random.choice(sp_char))

    pwd_fi = pwd_wrd + pwd_num + pwd_sym

    random.shuffle(pwd_fi)
    pwd_fi = ''.join(pwd_fi)

    return pwd_fi


if __name__ == '__main__':
    wrd_len, sym_len, num_len = get_usr_in()
    nw_pwd = gen_pwd(wrd_len, sym_len, num_len)

    print(nw_pwd)




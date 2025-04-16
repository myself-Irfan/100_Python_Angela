import logging

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHashError


ph = PasswordHasher()


def hash_pwd(pwd_str: str) -> str:
    return ph.hash(pwd_str)

def verify_pwd(pwd_hashed: str, pwd_str: str) -> bool:
    try:
        ph.verify(pwd_hashed, pwd_str)
        return True
    except VerifyMismatchError as ver_err:
        logging.warning(f'VerifyMismatch Error: {ver_err}')
    except InvalidHashError as invalid_err:
        logging.error(f'InvalidHashError: {invalid_err}')
    except Exception as err:
        logging.error(f'Unexpected error: {err}')
    return False
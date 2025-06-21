import json
import os
import logging


def setup_logging(cur_f_name: str) -> None:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s -> %(funcName)s | %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(f'{cur_f_name}.log')
        ]
    )

    logging.info('Logging setup complete')


def read_json_f(json_f: str) -> dict:
    try:
        logging.info(f'Trying to read file: {json_f}')
        with open(json_f, 'r') as json_file:
            return json.load(json_file)
    except FileNotFoundError as notfound_err:
        logging.error(f'{json_f} not found: {notfound_err}')
    except json.JSONDecodeError as json_decode_err:
        logging.error(f'JSON decode error: {json_decode_err}')
    except Exception as err:
        logging.error(f'Unexpected error: {err}')

    return {'error': 'Failed to load JSON'}


def get_morse(morse_dict: dict, user_char: str) -> str:
    logging.debug(f'Received char: {user_char}')

    morse_char = morse_dict.get(user_char)

    if morse_char is None:
        logging.warning(f'Character {user_char} not found in JSON dictionary')
        return '?'

    return morse_char


def get_morse_str(morse_dict: dict, user_str: str) -> str:
    logging.info('Initiating conversion')

    morse_str = []
    unknown_cnt = 0
    for user_char in user_str:
        morse_char = get_morse(morse_dict, user_char.upper()) + ' '
        if morse_char == '?':
            unknown_cnt += 1
        morse_str.append(morse_char)

    if unknown_cnt:
        logging.warning(f'Encountered {unknown_cnt} unknown chars during conversion')

    logging.info(f'Encrypted morse code: {''.join(morse_str)}')
    return ''.join(morse_str)


def main():
    setup_logging(CUR_F_NAME)
    logging.info('Program initiating...')

    morse_dict = read_json_f(JSON_FILE)
    if 'error' in morse_dict:
        logging.critical('Morse dictionary failed to lead. Terminating program...')
        return

    user_in = input('Provide your input: ').strip()
    logging.info(f'User provided: {user_in}')
    if not user_in:
        logging.info('No input provided. Terminating program...')
        return

    morse_str = get_morse_str(morse_dict, user_in)

    print(f'{user_in} -> {morse_str}')
    logging.info('Reached end of execution. Program terminating...')


if __name__ == '__main__':
    CUR_F_NAME = os.path.splitext(os.path.basename(__file__))[0]
    JSON_FILE = 'input-82.json'

    main()

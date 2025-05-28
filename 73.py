import pandas as pd
import os
import logging


def setup_logging(cur_f_name: str) -> None:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(funcName)s | %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(f'{cur_f_name}.log')
        ]
    )

    logging.info('Logging setup complete')


def fetch_df(location: str) -> pd.DataFrame | None:
    logging.info(f'Attempting to read CSV file from {location}')

    try:
        df = pd.read_csv(location, header=0, names=COLUMN_NAMES)
    except FileNotFoundError as notfound_err:
        logging.warning(f"File not found: {notfound_err}")
        return None
    except Exception as err:
        logging.error(f'Unexpected error: {err}')
        return None
    else:
        return df


if __name__ == '__main__':
    cur_f_name = os.path.splitext(os.path.basename(__file__))[0]
    COLUMN_NAMES = ['DATE', 'TAG', 'POSTS']

    setup_logging(cur_f_name)
    df = fetch_df(f'input-{cur_f_name}.csv')

    if df.empty:
        logging.warning(f'Built dataframe is empty. Exiting...')
        exit()

    logging.info(f'Top 5:\n{df.head(5)}\n Low 5:\n{df.tail(5)}')
    logging.info(f'Rows: {df.shape[0]}\t Column: {df.shape[1]}')
    logging.info(f'Column count:\n{df.count()}')

    total_lang_post = df.groupby('TAG')[['POSTS']].sum()
    logging.info(f'Total Post Per Language:\n{total_lang_post}')

    top_lang_tag = total_lang_post['POSTS'].idxmax()
    top_lang_count = total_lang_post['POSTS'].max()
    logging.info(f'Top Language Tag: {top_lang_tag} Count: {top_lang_count}')

    total_lang_per_month = df.groupby('TAG')[['POSTS']].count()
    logging.info(f'Post per month each lang: {total_lang_per_month}')
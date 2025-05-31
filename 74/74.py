import os
import logging
import pandas as pd


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


def fetch_df(csv_in: str) -> pd.DataFrame:
    logging.info(f'Fetching DataFrame from {csv_in}')

    try:
        df = pd.read_csv(csv_in, index_col=0)
    except FileNotFoundError as notfound_err:
        logging.error(f'File not found: {csv_in}')
        raise notfound_err
    except pd.errors.EmptyDataError as empty_err:
        logging.error(f'Empty data in file: {csv_in}')
        raise empty_err
    except pd.errors.ParserError as parse_err:
        logging.error(f'Error parsing file: {csv_in}')
        raise parse_err
    except Exception as e:
        logging.error(f'An unexpected error occurred: {e}')
        raise e
    else:
        logging.info(f'DataFrame fetched successfully with {len(df)} rows and {len(df.columns)} columns')
        return df
    

def main():
    color_df = fetch_df('data/colors.csv')
    logging.info(f'Unique colors: {color_df.name.nunique()}')
    logging.info(f'Number of transparent colors: {color_df.is_trans.value_counts()}')

    sets_df = fetch_df('data/sets.csv')
    logging.info(f'First year set details:\n{sets_df[sets_df.year == sets_df.year.min()]}')
    logging.info(f'Top 5 sets with most number of parts: {sets_df.sort_values("num_parts", ascending=False).head(5)}')


if __name__ == '__main__':
    setup_logging(os.path.splitext(os.path.basename(__file__))[0])

    main()
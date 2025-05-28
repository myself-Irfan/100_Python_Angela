import pandas as pd
import os
import logging


def setup_logging(cur_f_name: str):
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
        df = pd.read_csv(location)
    except FileNotFoundError as notfound_err:
        logging.warning(f"File not found: {notfound_err}")
        return None
    except Exception as e:
        logging.error(f'Unexpected error: {e}')
        return None
    else:
        return df


if __name__ == "__main__":
    cur_f_name = os.path.splitext(os.path.basename(__file__))[0]

    setup_logging(cur_f_name)
    
    df = fetch_df('72-input.csv')
    if df is None:
        logging.error('DataFrame is None, exiting...')
        exit()

    logging.info(f'DataFrame loaded!')
    # logging.info(f'Row: {(df.shape[0])}\tColumn: {(df.shape[1])}\nColumn attribute: {df.columns}')

    if df.isna:
        logging.info('There is empty')
        df = df.dropna()

    max_starting_idx = df["Starting Median Salary"].idxmax()
    logging.info(f'Max starting median salary {df["Starting Median Salary"].max()} is for major: {df["Undergraduate Major"].loc[max_starting_idx]}')

    max_mid_idx = df['Mid-Career Median Salary'].idxmax()
    logging.info(f'Max mid-career median salary: {df['Mid-Career Median Salary'].max()} for major: {df["Undergraduate Major"].loc[max_mid_idx]}')

    min_starting_idx = df["Starting Median Salary"].idxmin()
    logging.info(f'Min starting median salary: {df["Starting Median Salary"].min()} is for major: {df["Undergraduate Major"].loc[min_starting_idx]}')

    logging.info(f'Medium Mid-career salary details: \n{df.loc[df['Mid-Career Median Salary'].idxmin()]}')

    df['Spread'] = df['Mid-Career 90th Percentile Salary'] - df['Mid-Career 10th Percentile Salary']

    highest_potential = df.sort_values(by=["Mid-Career 90th Percentile Salary"], ascending=False)
    logging.info(f'Top 5 highest potential\n {highest_potential[['Undergraduate Major', 'Spread']].head(5)}')

    df = df.sort_values(by=['Spread'], ascending=False)
    logging.info(f'Top 5 greatest spread\n{df[['Undergraduate Major', 'Spread']].head(5)}')

    logging.info(f'{df.columns}')

    summary_df = df.groupby('Group')[
        [
            'Starting Median Salary',
            'Mid-Career Median Salary',
            'Mid-Career 10th Percentile Salary',
            'Mid-Career 90th Percentile Salary'
        ]
    ].mean()
    pd.options.display.float_format = '{:,.2f}'.format
    logging.info(f'Group ->\n{summary_df}')

    df.to_csv(f'{cur_f_name}-result.csv', index=None)
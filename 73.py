import pandas as pd
import os
import logging
import matplotlib.pyplot as plt


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

    # converting date str to datetime
    df['DATE'] = pd.to_datetime(df['DATE'])

    reshaped_df = df.pivot(index='DATE', columns='TAG', values='POSTS')
    logging.info(f'Pivot Columns: {reshaped_df.columns}')
    logging.info(f'Pivot Table Entry Count: {reshaped_df.count()}')
    reshaped_df = reshaped_df.fillna(0)
    logging.info(f'Pivot Rows: {reshaped_df.shape[0]}\tColumns: {reshaped_df.shape[1]}')
    logging.info(f'Pivot top 5 rows:\n{reshaped_df.head(5)}')
    logging.info(f'Pivot low 5 rows:\n{reshaped_df.tail(5)}')

    logging.info(f'NaN in pivot df: {reshaped_df.isna().values.any()}')

    # check 12
    chart_df = reshaped_df.rolling(window=12).mean()

    plt.figure(figsize=(15, 10))
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.xlabel('Date', fontsize=15)
    plt.ylabel('Number of Posts', fontsize=15)
    # plt.ylim(0, 35000)
    # plt.plot(reshaped_df.index, reshaped_df.java)
    # plt.plot(reshaped_df.index, reshaped_df.python)

    for column in chart_df.columns:
        plt.plot(
            chart_df.index,
            chart_df[column],
            linewidth=3,
            label=chart_df[column].name
        )
    plt.legend(fontsize=15)

    plt.show()

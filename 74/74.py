from pathlib import Path
import logging
import pandas as pd
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


def plot_df(x_data, y_data, title: str, x_label: str, y_label: str):
    logging.info(f'Initiating plotting chart')

    if len(x_data) != len(y_data):
        logging.error(f'x_data: {x_data} and y_data: {y_data} must be of same length')
        return

    if x_data.empty or y_data.empty:
        logging.warning(f'x_data: {x_data} or y_data: {y_data} is empty')
        return

    try:
        plt.figure(figsize=(15, 10))
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)
        plt.title(title)
        plt.xlabel(x_label, fontsize=15)
        plt.ylabel(y_label, fontsize=15)
        plt.plot(x_data, y_data, marker='o')
        plt.grid(True)
        plt.tight_layout()
        plt.show()

        logging.info('Plotting complete')
    except Exception as e:
        logging.error(f'Unexpected error: {e}')


def plot_twinx_line_chart(x_data, y1_data, y2_data, title:str, x_label: str, y1_label: str, y2_label: str):
    logging.info('Initiating plotting twin-x chart')

    if not (len(x_data) == len(y1_data) == len(y2_data)):
        logging.error(f'x_data: {x_data}, y1_data: {y1_data} and y2_data: {y2_data} must be of same length')
        return

    if any(len(data) == 0 for data in [x_data, y1_data, y2_data]):
        logging.warning(f'One or more data inputs are empty. x_data: {x_data}, y1_data: {y1_data}, y2_data: {y2_data}')
        return

    try:
        fig, ax1 = plt.subplots(figsize=(15, 10))
        ax2 = ax1.twinx()

        ax1.plot(x_data, y1_data, color='g', marker='o', label=y1_label)
        ax2.plot(x_data, y2_data, color='b', marker='o', label=y2_label)

        ax1.set_xlabel(x_label, fontsize=15)
        ax1.set_ylabel(y1_label, fontsize=15)
        ax2.set_ylabel(y2_label, fontsize=15)
        ax1.set_title(title, fontsize=18)

        ax1.tick_params(axis='x', labelsize=10)
        ax1.tick_params(axis='y', labelsize=10)
        ax2.tick_params(axis='y', labelsize=10)
        ax1.grid(True)

        plt.tight_layout()
        plt.show()

        logging.info('Plotting complete')
    except Exception as e:
        logging.error(f'Unexpected error: {e}')


def main():
    color_df = fetch_df('data/colors.csv')
    logging.info(f'Unique colors: {color_df.name.nunique()}')
    logging.info(f'Number of transparent colors: {color_df.is_trans.value_counts()}')

    sets_df = fetch_df('data/sets.csv')
    sets_df = sets_df.reset_index()
    logging.info(f'First year set details:\n{sets_df[sets_df.year == sets_df.year.min()]}')
    logging.info(f'Top 5 sets with most number of parts: {sets_df.sort_values("num_parts", ascending=False).head(5)}')

    sets_by_yr = sets_df.groupby('year')[['set_num']].count().sort_values(by=['year'], ascending=True)
    logging.info(f'Earliest 5 sets release: {sets_by_yr.head(5)}')
    logging.info(f'Latest 5 sets release: {sets_by_yr.tail(5)}')

    plot_df(
        x_data=sets_by_yr.index[:-2],
        y_data=sets_by_yr.set_num[:-2],
        title='Number of Sets Released by Year',
        x_label='Year',
        y_label='Number of Sets'
    )

    themes_by_yr = sets_df.groupby('year').aggregate({'theme_id': pd.Series.nunique})
    themes_by_yr = themes_by_yr.rename(columns={'theme_id': 'num_themes'})
    logging.info(f'Earliest 5 theme by year:\n{themes_by_yr.head(5)}')
    logging.info(f'Latest 5 theme by year:\n{themes_by_yr.tail(5)}')

    plot_df(
        x_data=themes_by_yr.index[:-1],
        y_data=themes_by_yr.num_themes[:-1],
        title='Theme by Year',
        x_label='Year',
        y_label='Theme count'
    )

    plot_twinx_line_chart(
        x_data=sets_by_yr.index[:-2],
        y1_data=sets_by_yr.set_num[:-2],
        y2_data=themes_by_yr.num_themes[:-2],
        title='Set vs Themes over the years',
        x_label='Year',
        y1_label='Number of Sets',
        y2_label='Number of Themes'
    )


if __name__ == '__main__':
    setup_logging(Path(__file__).stem)

    main()
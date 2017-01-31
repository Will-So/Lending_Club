"""
Calculates the rate of return for each cohort. This will be useful for establishing the correlation with the stock market.

Methodology: Do quarterly and then up-sample to monthly to compare with S&P 500 returns.

Situation
---
- For each quarter
- Invest in 400 Notes in a quarter (Sample without replacement)
- Sample notes by quarter N times (100 is probably sufficient)
"""

from scripts.clean_data import SAVE_DIR, SAVE_TYPE
from collections import defaultdict
import pickle

import pandas as pd

SAVE = False


def _main():
    df = load_data()
    df = get_quarterly_periods(df)
    categories = df.bin.cat.categories # We need these categories in future
    samples = sample_values(df)
    if SAVE:
        save_samples(samples, SAVE_DIR)

    del df # All the data needed is in samples
    returns =
    if SAVE:
        pickle.dump(returns, open(SAVE_DIR + 'returns.pkl', 'wb'))

    average_returns =



def load_data():
    """

    :return: dataframe
    """
    df = pd.read_pickle(SAVE_DIR + '/cleaned_df.pkl')
    df = df.query('int_rate > .16')

    return df


def get_quarterly_periods(df):
    """
    Creates the bins that the data will be

    :return:
    """
    year_quarter_pairs = list(zip(df.issue_d.dt.year.values,
                                  df.issue_d.dt.quarter.values))

    complete_date = ['.'.join(map(str, i)) for i in year_quarter_pairs]

    df['bin'] = complete_date
    df['bin'] = df['bin'].astype('category')

    ## Consider only values that are frequent enough to be factor
    counts = df.bin.value_counts()
    df = df.loc[df.bin.isin(counts[counts > 750].index)]
    df.bin = df.bin.cat.remove_unused_categories()

    return df


def sample_values(df):
    """
    Create a sample of 250 notes for every cohort. Takes about 2 minutes
    to run on a 2015 macbook pro

    :return: dictionary of form
    {'2014.1': {{1:df1}, {2:df2}, ... }
    {'2014.2': {{1: df1}, .. }}}
    """
    samples = tree()
    num_simulations = 100
    for cat in df.bin.cat.categories:
        for simulation in range(num_simulations):
            sample_df = df.query('bin == @cat')
            sample_df = sample_df.sample(400, replace=False)
            samples[cat][simulation] = sample_df


def save_samples(samples, save_dir):
    """
    Saves the

    :param samples: dict containing all of the sampels of 250 notes
    :return:
    """
    pickle.dump(samples, open(save_dir + 'samples.pkl', 'wb'))


def tree():
    """
    Allows creating a nested dictionary and avoids keyerrors.

    :return:
    """
    return defaultdict(tree)

def calculate_roi(samples):
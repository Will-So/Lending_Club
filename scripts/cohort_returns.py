"""
Calculates the rate of return for each cohort. This will be useful for establishing the correlation with the stock market.

Methodology: Do quarterly and then up-sample to monthly to compare with S&P 500 returns.

Situation
---
- For each quarter
- Invest in 400 Notes in a quarter (Sample without replacement)
- Sample notes by quarter N times (100 is probably sufficient)
"""

import sys
sys.path.append('..')
import pickle
import numpy as np
import pandas as pd

from scripts.clean_data import SAVE_DIR, SAVE_TYPE
from collections import defaultdict


SAVE = False
LOAD = True


def _main():
    df = load_data(term=36)
    df = get_quarterly_periods(df)
    df.bin = df.bin.cat.remove_unused_categories()
    categories = df.bin.cat.categories # We need these categories in future
    if LOAD:
        samples = load_samples(SAVE_DIR)
    else:
        samples = sample_values(df, term=36)

        if SAVE: # Only want to save samples if we computed them again
            save_samples(samples, SAVE_DIR)

    del df # All the data needed is in samples
    total_returns, roi_dict = consolidate_returns(samples, term=3)

    if SAVE:
        pickle.dump(roi_dict, open(SAVE_DIR + 'all_returns.pkl', 'wb'))
        pickle.dump(total_returns, open(SAVE_DIR + 'consolidated_returns.pkl', 'wb'))




def load_data(term):
    """

    :return: dataframe
    """
    df = pd.read_pickle(SAVE_DIR + '/cleaned_df.pkl')
    if term:
        df = df.query('term == @term')
    df = df.query('int_rate > .16')

    return df


def load_samples(save_dir):
    """
    Loads the dictionary of samples that was previous saved

    :return: samples; dict of dataframes
    """

    return pickle.load(open(save_dir + 'samples.pkl', 'rb'))


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


def sample_values(df, term=None):
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
            if term:
                df = df.query('term == @term')

            sample_df = df.query('bin == @cat')
            sample_df = sample_df.sample(400, replace=False)

            samples[cat][simulation] = sample_df

    return samples


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


def calculate_roi(df, term=36):
    """
    Calculate the return rate according to the following formula

    $$ \frac{total\_pymnt - loan\_amnt}{loan\_amnt} * \frac{1}{term} $$


    :param term: the term that all of the loans belong in
    :param df: dataframe to calculate total return
    :return: roi for the entire sample
    """
    assert int(df.term.mean()) == term
    total_payment = df.total_pymnt.sum()
    total_loan_amount = df.loan_amnt.sum()
    total_roi = ((total_payment - total_loan_amount) / total_loan_amount) * (1 / (term / 12)) # 12 for the number of years

    return total_roi


def consolidate_returns(samples, term):
    """

    :param samples:
    :return: total_roi, a dict of the average roi of each cohort.
             roi_dict, all individual ROI values. Good for sampling the values
    """
    roi_dict = tree() # This is here mostly for debugging
    total_roi = dict() # This is the value we're interested in and actually going to return

    # Get the ROI for each value
    for cohort in samples.keys():
        for sample in samples[cohort].keys():
            print(cohort, '\t', sample)
            roi_dict[cohort][sample] = calculate_roi(samples[cohort][sample], term)
        cohort_average = np.mean([roi_dict[cohort][i] for i
                                    in roi_dict[cohort].keys()])
        total_roi[cohort] = cohort_average

    return total_roi, roi_dict



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

import pandas as pd


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

    return df


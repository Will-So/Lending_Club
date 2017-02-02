"""
Loads all lending Club CSV Files, Cleans the data for future analysis,
adds some features and then saves it to csv and optionally pickle.

We save it to csv for use with Pickle. We save it to
"""

import pandas as pd
import numpy as np
import os
import warnings
import feather
warnings.simplefilter("ignore") # Pandas is setting up annoying filters

# DATA_DIR = '/Users/wsorenson/data_2016/lc/'
SAVE_TYPE = 'Pickle'# Add option for Pickle because of categorical variables
# SAVE_DIR = os.path.join(DATA_DIR, 'processed')
DATA_DIR = '/Volumes/base/data/lc_data/'
SAVE_DIR = os.path.join(DATA_DIR, 'processed')
FILTER_DATE = '2014-09-01' # This is the date that we want to consider when filtering the results.


def _main():
    print("Loading Data")
    df = pd.DataFrame()
    # TODO This should check to only open proper csv files
    # TODO not reading all files for some reason
    for csv in os.listdir(DATA_DIR)[:-1]:
        df = df.append(pd.read_csv(DATA_DIR + csv, header=1)) ## LC added a 1 line disclaimer on their csv file.
        print("Loaded file {}".format(csv))

    # TODO: Don't want important columns in this workflow. Put this in a consants page.
    important_columns = ['total_pymnt', 'zip_code', 'member_id', 'id', 'loan_amnt', 'int_rate',
         'installment', 'emp_length', 'home_ownership', 'grade', 'sub_grade', 'emp_title',
         'issue_d', 'loan_status', 'annual_inc', 'verification_status', 'purpose', 'addr_state',
         'inq_last_6mths', 'dti', 'revol_util', 'mths_since_last_delinq','pub_rec', 'revol_bal',
         'open_acc', 'collections_12_mths_ex_med', 'delinq_2yrs', 'earliest_cr_line',
         'fico_range_low', 'last_credit_pull_d', 'term']

    df = df[important_columns]

    df = df[:-2] # The last 2 rows of the CSV arent proper rows

    df = clean_columns(df)

    df = additional_features(df)

    if SAVE_TYPE == 'Pickle':
        print('saving to pickle')
        df.to_pickle(os.path.join(SAVE_DIR, 'cleaned_df.pkl'))
    elif SAVE_TYPE == 'Feather':
        print('Saving to Feather')
        raise NotImplementedError("Haven't added feather yet")
    else:
        print("Saving to CSV")
        df.to_csv(os.path.join(SAVE_DIR, 'cleaned_df.csv'))


def clean_columns(df):
    """
    Changes columns to appropriate types and removes certain annoying rows.

    :param df: pd.Dataframe
    :return: pd.DataFrame with cleaned columns
    """
    print("Cleaning Columns. This takes minutes due to a large number of string"
          " operations.")

    df['zip_code'] = df['zip_code'].str.replace('x', '')

    df.id = df.id.astype(str)
    df = df[~df.id.str.contains('[A-z]', na=False)] # Remove ids with words
    df['id'] = df.id.astype(int)

    # Change employment length to inits
    df.emp_length = df.emp_length.replace({'10+ years': 20, '< 1 year': 0, '1 year': 1})
    df.emp_length = df.emp_length.replace({'{} years'.format(i): i
                                           for i in range(1,10)})

    df.emp_length = df.emp_length.replace({'n/a': np.nan})

    df.int_rate = df.int_rate.str.replace('%', '').astype(float) / 100
    df['revol_util'] = df.revol_util.str.replace("%", '').astype(float) / 100

    df.home_ownership = df.home_ownership.astype('category')

    # Change the subgrades to numeric values
    unique_subgrades = sorted(df.sub_grade.unique())
    df.sub_grade = df.sub_grade.replace({'{}'.format(i):
                      unique_subgrades.index(i) for i in unique_subgrades})

    # Turn dates into datetime objects
    df.issue_d = pd.to_datetime(df.issue_d)
    df.earliest_cr_line = pd.to_datetime(df.earliest_cr_line)
    df.last_credit_pull_d = pd.to_datetime(df.last_credit_pull_d)

    if FILTER_DATE: # We may not always want to get rid of items
        df = df[df.issue_d < FILTER_DATE] # See (1) in methodology

    # Turn the term into strings of the duration
    df = df[df.term.notnull()]
    df.term = df.term.str.extract('(\d+)').astype('int')

    df.verification_status = df.verification_status.replace({'VERIFIED - income': 1,
                                'VERIFIED - income source': 1, 'not verified': 0 })
    df.verification_status = df.verification_status.astype('category')

    # The following loans will not be useful for our analysis. See §2 in methodology
    df = df[~df.loan_status.str.contains("Does not meet the credit policy")]

    df = category_processing(df)
    print("Finished cleaning columns; creating additional features")

    return df


def category_processing(df):
    """
    Ensure that all categories are present in the data provided by API.
    """

    df.grade = df.grade.astype('category')
    df.zip_code = df.zip_code.astype('category')
    df.purpose = df.purpose.astype('category')
    df.addr_state = df.addr_state.astype('category')

    # Can't make predictions based off of loans that cannot be reissued
    df.loan_status = df.loan_status.astype('category')

    df.loc[df.home_ownership.isin(['NONE', 'ANY']), 'home_ownership'] = 'OTHER'
    df.home_ownership = df.home_ownership.cat.remove_unused_categories()
    df.zip_code = df.zip_code.cat.remove_unused_categories()

    return df


def additional_features(df):
    """
    Creates additional features that may be important

    :param df: pd.DataFrame
    :return: df with added columns.
    """
    print("Adding new features")

    df['ratio_inc_debt'] = (df.loan_amnt + df.revol_bal) / df.annual_inc
    df['ratio_inc_installment'] = df.installment / (df.annual_inc / 12)
    df['ratio_mth_inc_all_payments'] = (df.installment + df.revol_bal * .02) / (df.annual_inc / 12)
    df['year_issued'] = df.issue_d.dt.year
    df['month_issued'] = df.issue_d.dt.month

    df['earliest_cr_line'] = df.earliest_cr_line.dt.year # We are only interested in the year here
    oldest_line = df.earliest_cr_line.min()
    df.earliest_cr_line = df.earliest_cr_line.apply(lambda x: x - oldest_line)

    df['delinq']= 0
    df['delinq'][df.loan_status.isin(['Charged Off', 'Late (31-120 days)',
                                      'Default'])] = 1

    return df

if __name__ == '__main__':
    _main()
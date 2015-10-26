import pandas as pd
import numpy as np
import os
import sys
DATA_DIR = '/Users/Will/Data/lending_club/'


def _main():
    df = pd.DataFrame()
    for csv in os.listdir(DATA_DIR)[1:]:
        df = df.append(pd.read_csv(DATA_DIR + csv, header=True))

    important_columns = ['total_pymnt', 'zip_code', 'member_id', 'id', 'loan_amnt', 'int_rate',
         'installment', 'emp_length', 'home_ownership', 'grade', 'sub_grade', 'emp_title',
         'issue_d', 'loan_status', 'annual_inc', 'verification_status', 'purpose', 'addr_state',
         'inq_last_6mths', 'dti', 'revol_util', 'mths_since_last_record', 'mths_since_last_delinq',
         'pub_rec', 'revol_bal', 'open_acc', 'collections_12_mths_ex_med', 'delinq_2yrs',
         'earliest_cr_line',  'last_credit_pull_d']
    df = df[important_columns]

    df = df[:-2] # The last 2 rows of the CSV arent proper rows

    df = clean_columns(df)


def clean_columns(df):
    """

    :param df: Dataframe
    :return:
    """
    df['zip_code'] = df['zip_code'].str.replace('x', '')
    df.zip_code = df.zip_code.astype('category')
    df = df[~df.id.str.contains('[A-z]', na=False)] #Remove ids with words
    df['id'] = df.id.astype(int)

    # Change employment length to inits.
    df.emp_length = df.emp_length.replace({'10+ years': 20, '< 1 year': 0, '1 year': 1})
    df.emp_length = df.emp_length.replace({'{} years'.format(i): i
                                           for i in range(1,10)})
    df.emp_length = df.emp_length.replace({'n/a': np.nan})

    df.int_rate = df.int_rate.str.replace('%', '').astype(float) / 100

    df.home_ownership = df.home_ownership.astype('category')

    # Change the subgrades to numeric values
    unique_subgrades = sorted(df.sub_grade.unique())
    df.sub_grade = df.sub_grade.replace({'{}'.format(i):
                      unique_subgrades.index(i) for i in unique_subgrades})

    df['grade'] = df['grade'].astype('category')
    df.loan_status = df.loan_status.astype('category')


    df.issue_d = pd.to_datetime(df.issue_d)


    return df

if __name__ == 'main':
    sys.exit(_main())
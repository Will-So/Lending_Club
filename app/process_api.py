"""
The API diverges to an annoying extent from the provided dataset. This is an attempt to
remedy the differences.

Some overlap with the `clean_data` module is inevitable.

There are also plenty of opportunities to break this API

Steps:
    1. Load the Latest Notes from lending club `generate_completed_df()`
    2. Rename and Process the Columns to be consistent with the previous dataset
    3. Create the y, X matrix from the columns
    4. Load the Model
    5. Predict the Probabilities of default
    6. Calculate the projected ROI into a dataframe
    7. Return the df with the new fields
"""

import sys
import requests
import os
import pandas as pd
import numpy as np
import re
import pickle
import arrow

from sklearn.externals import joblib


sys.path.append("../scripts")
from model import create_matrix

PICKLE = False
DEBUG = True

def generate_completed_df():
    """
    Gathers the top choices from the currently available lending club notes.

    We handle the unexpected values before creating the X matrix because the rows won't lone up otherwise

    :return: dataframe that is processed and has the proper number of ROI features.
    """
    df = load_latest_notes()
    df = rename_columns(df)
    df = process_columns(df)
    df = handle_unexpected_values(df)
    y, X = create_matrix(df)

    model = joblib.load('../model/rf_model.pkl')

    predict_prob = model.predict_proba(X)

    top_choices = top_predict_roi(df, predict_prob)
    pretty_top_choices = format_df(top_choices)

    if PICKLE:
        pretty_top_choices.to_pickle('../API_df')

    return pretty_top_choices


def load_latest_notes():
    """
    Retrieves currently available notes from the Lending Club API
    """
    credentials = os.environ['LENDING_CLUB_API']

    headers = {'Authorization': credentials}

    r = requests.get('https://api.lendingclub.com/api/investor/v1/loans/listing?showAll=true',
                headers=headers)

    assert r.status_code == 200

    loans = r.json()['loans']
    df = pd.DataFrame(loans)
    return df


def rename_columns(df):
    """
    renames certain columns and fills in certain static values
    (e.g., current month, year)
    """
    df['year_issued'] = 2015
    current_month = arrow.utcnow().month
    assert type(current_month) == int
    df['month_issued'] = current_month
    df['delinq'] = 2 # Needs to be something for the create_matrix method; discarded later

    df.columns = [convert(i) for i in df.columns]

    df = df.rename(columns={'collections12_mths_ex_med': 'collections_12_mths_ex_med',
                            'loan_amount': 'loan_amnt', 'delinq2_yrs': 'delinq_2yrs',
                            'inq_last6_mths':'inq_last_6mths', 'addr_zip':'zip_code'})

    return df


def process_columns(df):
    """
    Deals with the non-trivial inehrent incompatibility between the lending club API and the
    lending club dataset. (yes you read that right).

    :param df: Pandas DataFrame
    :return: Pandas Dataframe that is more compatible with the historical dataset
    """
    df.emp_length /= 12

    df['ratio_mth_inc_all_payments'] = (df.installment + df.revol_bal * .02) / (df.annual_inc / 12)

    df.int_rate /= 100
    df.revol_util /= 100

    df.addr_state = df.addr_state.astype('category')

    # Extracts the year from earliest_cr_line column
    df.earliest_cr_line = df.earliest_cr_line.astype(np.datetime64).dt.year.astype(int)

    df = consolidate_categoricals(df)

    df.emp_length = df.emp_length.fillna(1) # Many people do not yet have their

    return df


def consolidate_categoricals(df):
    """
    Consolidates categories between the trained model and data gotten from the API

    # TODO: This can be somewhat automated The steps are as follows
        1. Make sure that the item is a category now
        2. Find the set difference between the 'complete' set and the incomplete set
        3. (optional) remove data points that don't conform to the reference set
        4. Add the category to it

    :param df: pd.DataFrame populated with API data from Lending Club
    :return: df
    """

    # Service to LC is rather new and not included in the model so remove it
    df = df[df.addr_state != 'ND']
    try:
        df.addr_state = df.addr_state.cat.remove_categories(['ND'])
    except ValueError: # Deals with case when ND never was a category
        pass

    # Need to make sure all purposes are in the catories
    with open('../purpose_list.pkl', 'rb') as picklefile:
        reference_purposes = pickle.load(picklefile)

    new_purposes = reference_purposes - set(df.purpose.unique())
    df.purpose = df.purpose.astype('category')
    df.purpose = df.purpose.cat.add_categories(new_purposes)

    # Verify all states in categories
    with open('../state_list.pkl', 'rb') as picklefile:
        state_list = pickle.load(picklefile)

    unique_states = df.addr_state.unique()
    new_states = set(state_list) - set(unique_states.get_values())
    df.addr_state = df.addr_state.cat.add_categories(new_states)

    # Make 'other' category even though no longer used
    df.home_ownership = df.home_ownership.astype('category')
    df.home_ownership = df.home_ownership.cat.add_categories(['OTHER'])

    # Make sure all grades present
    df.grade = df.grade.astype('category')
    new_grades = {'A', 'B', 'C', 'D', 'E', 'F', 'G'} - set(df.grade.unique())
    df.grade = df.grade.cat.add_categories(new_grades)

    return df


def top_predict_roi(df, probabilities, percentage=.25):
    """
    Predicts ROI of notes and returns the best

    :param df:
    :param probabilities: Estimated default probability from SKLearn classification alrogithims.
    N X 2 matrix where the first column the probability of not defaulting and the second is the
    probability of defaulting.
    :param percentage: percentage of Dataframes to select
    :return: Pandas Dataframe with the top choices

    Notes
    ---
    - `estimated_roi` is calculated according to the following formula:
    $(1 - p(default) * (int\_rate - fee)
        + p(default) * percent\_lost / avg_\term $

    This is meant to be more conservative than average. Picking the top 20% of loans is likely to have
    a return of 13.5% rather than 10%. Rank-order is preserved.

    Example
    ---
    >>> top_predict_roi(df, probabilities) # DOCTEST: +SKIP
    """

    probabilities =  [i[1] for i in probabilities]
    df['default_prob'] = probabilities

    df['estimated_roi'] = ((1 - df.default_prob) * (df.int_rate - 0.0060)
                                + (df.default_prob * ((-0.55 * df.loan_amnt) / df.loan_amnt) / 3.5))

    sorted_df = df.sort_values('estimated_roi', ascending=False)

    top_choices = sorted_df[:int(len(sorted_df) * percentage)]

    if DEBUG:
        top_choices.to_csv('../top_choices.csv')
        sorted_df.to_csv('../sorted_df.csv')

    return top_choices


def format_df(df):
    """
    Formats the df so important columns come first.

    """

    model_columns = ['loan_amnt', 'int_rate', 'grade',  'installment' , 'emp_length', 'home_ownership' ,
                'purpose', 'addr_state' , 'inq_last_6mths', 'pub_rec' , 'revol_bal',
                 'open_acc', 'collections_12_mths_ex_med','delinq_2yrs', 'annual_inc',
                 'earliest_cr_line', 'fico_range_low', 'ratio_mth_inc_all_payments',
                     'estimated_roi', 'default_prob']

    unimportant_columns = ['addr_state', 'pub_rec', 'open_acc',
                           'inq_last_6mths', 'collections_12_mths_ex_med']

    important_columns = [i for i in model_columns if i not in unimportant_columns]
    important_columns.insert(0, 'id') # Necessary to order the things later

    df = df[important_columns]

    # Hacky way to change the order of the columns
    cols = df.columns.tolist()
    cols = cols[0:1] + cols[-2:] + cols[1:-2] # [0:1] to prevent coercion to str
    df = df[cols]

    df = df.rename(columns={'ratio_mth_inc_all_payments': 'Payments/Income',
                                'fico_range_low':'fico'})

    return df


def handle_unexpected_values(df):
    """
    Handle various edge cases

    :param df: Pandas dataframe of features. (Usually X)
    :return: dataframe with edge cases handled
    """
    df = df[df.ratio_mth_inc_all_payments != np.inf]

    return df


def convert(name):
    """
    Helper function to change camelCase to camel_case. Function is just a first step,
    additional munging is required.

    Copied from http://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-camel-case
    :param name:
    :return:
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


if __name__ == '__main__':
    sys.exit(generate_completed_df())
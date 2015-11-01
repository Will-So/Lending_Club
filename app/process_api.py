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
    7. Return the df of
"""

import sys
import requests
import os
import pandas as pd
import numpy as np
import re
import pickle

import pdb

from sklearn.externals import joblib


sys.path.append("../scripts")
from model import create_matrix
from clean_data import clean_columns, category_processing


PICKLE = True


def generate_completed_df():
    """

    :return: dataframe that is processed and has the proper number of ROI features.
    """
    df = load_latest_notes()
    df = rename_columns(df)
    df = process_columns(df)
    y, X = create_matrix(df)
    model = joblib.load('../model/rf_model.pkl')

    predict_prob = model.predict_proba(X)
    print(len(y))
    print(df.head())
    pdb.set_trace() # Want to kill it here

    top_predict_roi(df, predict_prob)
    if PICKLE == True:
        df.to_pickle('API_df')

    return df


def load_latest_notes():
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

    :param df:
    :return:
    """
    df['year_issued'] = 2015
    df['month_issued'] = 11
    df['delinq'] = 2 # Needs to be something for the create_matrix method

    df.columns = [convert(i) for i in df.columns]

    df = df.rename(columns={'collections12_mths_ex_med': 'collections_12_mths_ex_med',
                            'loan_amount': 'loan_amnt', 'delinq2_yrs': 'delinq_2yrs',
                            'inq_last6_mths':'inq_last_6mths', 'addr_zip':'zip_code'})

    return df


def process_columns(df):
    """
    Deals with the non-trivial inehrent incompatibility between the lending club API and the
    lending club dataset. (yes you read that right).

    :param df:
    :return:
    """
    df.emp_length = df.emp_length / 12


    df['ratio_mth_inc_all_payments'] = (df.installment + df.revol_bal * .02) / (df.annual_inc / 12)

    df.int_rate = df.int_rate / 100
    df.revol_util = df.revol_util / 100

    df.home_ownership = df.home_ownership.astype('category')
    # ^^ Unused category in the API. This will probably make my life harder in other ways
    df.home_ownership = df.home_ownership.cat.add_categories(['OTHER'])

    df.addr_state = df.addr_state.astype('category')

    with open('../state_list.pkl', 'rb') as picklefile:
        state_list = pickle.load(picklefile)

    unique_states = df.addr_state.unique()
    new_states = set(state_list) - set(unique_states.get_values())
    df.addr_state = df.addr_state.cat.add_categories(new_states)

    # TODO: Generalize this pattern
    with open('../purpose_list.pkl', 'rb') as picklefile:
        reference_purposes = pickle.load(picklefile)
    new_purposes = reference_purposes - set(df.purpose.unique())
    df.purpose = df.purpose.astype('category')
    df.purpose = df.purpose.cat.add_categories(new_purposes)

    df.earliest_cr_line = df.earliest_cr_line.astype(np.datetime64).dt.year.astype(int)


    return df



def top_predict_roi(df, probabilities):
    """
    Given a df with default chance calculated, predicts the ROI of the note.

    The ROI formula is calculated according to the following formula:
    (1 - p(d)) * int_rate + p(d) * principal * (-0.55) // Need to work on this a bit more


    :return:
    """

    df['default_prob'] = probabilities

    loan_ids =  []

    return ids


def convert(name):
    """
    Helper function to change camelCase to camel_case.

    Copied from http://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-camel-case
    :param name:
    :return:
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


if __name__ == '__main__':
    sys.exit(generate_completed_df())
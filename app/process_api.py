"""
The API diverges to an annoying extent from the provided dataset. This is an attempt to
remedy the differences.

Some overlap with the `clean_data` module is inevitable.
"""

import sys
import requests
import os
import pandas as pd

sys.path.append("../scripts")
from model import create_matrix
from clean_data import clean_columns, category_processing

def generate_completed_df():
    """

    :return:
    """
    df = load_latest_notes()


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

def make_columns(df):
    """

    :param df:
    :return:
    """


def predict_default():
    """

    :return:
    """

if __name__ == '__main__':
    sys.exit(generate_completed_df())
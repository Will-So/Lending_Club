"""
Various sanity checks for the matrix
"""
import pandas as pd
import sys

sys.path.append("../app")

from process_api import load_latest_notes, rename_columns, process_columns, investor_id, headers

import requests
from .scripts.model import create_matrix


df = load_latest_notes()
df = rename_columns(df)
df = process_columns(df)


def diagnose_column_mismatch(df):
    reference_df = pd.read_pickle('../cleaned_df.pkl')
    reference_df = create_matrix(df)
    reference_set = set(reference_df.columns)
    df_set = set(df.columns)
    print('reference - df')
    print(reference_set - df_set)
    print('df - reference')
    print(df_set - reference_set)

diagnose_column_mismatch(df)


def get_portfolio_id():
    r = requests.get('https://api.lendingclub.com/api/investor/v1/accounts/{}/portfolios'
                     .format(investor_id), headers=headers)
"""
Tests whether the `process_api` module can handle weird values being fed to the dataframe

An interesting alternative is to run the tests as the dataframe is loaded.

"""
import py.test
import pandas as pd
import engarde.decorators as ed
import numpy as np
from hypothesis import given, assume, example, strategies as st


from app.process_api import generate_completed_df

test_df = generate_completed_df()


dtypes = dict(estimated_roi=float, default_prob=float, loan_amnt=float, int_rate=float,
              grade='category', installment=float, emp_length=float, home_ownership='category',
              purpose='category', revol_bal=float, delinq_2yrs=float, annual_inc=float,
              earliest_cr_line=int, fico=int, payments_to_income=float64)

def test_inf_values():
    """
    Ensures that all values are finite.

    Notes
    ---
    When processing the data from the API, the values that could cause np.inf should be removed
    automatically.
    """
    assert not any(np.isinf(test_df))


def test_categories():
    """
    Ensures that all categories are added to API even if not present in the API Data.
    """


@ed.is_shape((None, 16))
@ed.has_dtypes(items=dtypes)
def test_dtypes_and_shape():
    df = generate_completed_df()
    return df


@given(col=st.floats())
@example(col=0.0) # So that it is tested every time.
def test_valid_inputs(col):
    """Verufues that
    """
    df = generate_completed_df()
    assume(col >= 0)
    assert(all(df['Payments/Income'] > 0)) # Payments/Income depends on annual_income.

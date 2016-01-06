"""
Tests whether the `process_api` module can handle weird values being fed to the dataframe

An interesting alternative is to run the tests as the dataframe is loaded.

TODO:
- Test bad edge cases as well. Set it up so it is programmtically done.

"""
import py.test
import pandas as pd
import engarde.decorators as ed
import numpy as np
import sys
from hypothesis import given, assume, example, strategies as st


sys.path.append('../app')
from process_api import generate_completed_df

TEST_API = True
BAD_DATA = True

if TEST_API:
    test_df = generate_completed_df()
elif BAD_DATA:
    test_df = pd.read_csv('bad_data.csv')
else:
    test_df = pd.read_csv('good_data.csv')


dtypes = dict(estimated_roi=float, default_prob=float, loan_amnt=float, int_rate=float,
              grade='category', installment=float, emp_length=float, home_ownership='category',
              purpose='category', revol_bal=float, delinq_2yrs=int, annual_inc=float,
              earliest_cr_line=int, fico=int, payments_to_income=float)


def test_inf_values():
    """
    Ensures that all values are finite.

    Notes
    ---
    When processing the data from the API, the values that could cause np.inf should be removed
    automatically.
    """
    assert all(np.isfinite(test_df.select_dtypes(include=['float64', 'int64'])))


def test_categories():
    """
    Ensures that all categories are added to API even if not present in the API Data.
    """
    assert len(test_df.home_ownership.cat.categories) == 4
    assert len(test_df.purpose.cat.categories) == 14
    assert len(test_df.grade.cat.categories) == 7



@ed.is_shape((None, 16))
@ed.has_dtypes(items=dtypes)
def test_dtypes_and_shape():
    df = generate_completed_df()
    return df

def test_results_reasonable():
    """
    Verifies that various aspects of the dataset are reasonable
    """
    assert .05 < all(test_df.int_rate) < .4 # Interest rates should be within a reasonable range
    assert all(test_df.annual_inc) >= 0

    # TODO compare ROI to interest rate in each row



# @given(col=st.floats())
# @example(col=0.0) # So that it is tested every time.
# def test_valid_inputs(col):
#     """Verufues that
#     """
#     df = generate_completed_df()
#     assume(col >= 0)
#     assert(all(df['Payments/Income'] > 0)) # Payments/Income depends on annual_income.

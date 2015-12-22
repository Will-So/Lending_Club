"""
Tests whether the `process_api` module can handle weird values being fed to the dataframe
"""
import py.test
import engarde
import numpy as np


from app.process_api import generate_completed_df

test_df = generate_completed_df()

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


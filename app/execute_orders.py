"""
CLI that is meant to run in the background and place orders hourly.

Look into celery for doing this.
"""

import logging
from process_api import generate_completed_df

def get_load_ids():
    df = generate_completed_df()
    return list(df.id)

def place_order():
    """
    Places an order to
    
    :return:
    """

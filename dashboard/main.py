"""
Steps:
    1. Generate DF and predictions
    2. Display the App
"""
from bokeh.plotting import figure, show, output_server

from app.process_api import generate_completed_df

df = generate_completed_df()

p = figure(title="Predictions for Currently Available Notes")


def generate_aggregated_roi():
    """

    :return:
    """
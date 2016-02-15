"""
Steps:
    1. Generate DF and predictions
    2. Display the App
"""
from bokeh.plotting import figure, show, output_server

from bokeh.models.widgets import Slider, Select, TextInput, CheckboxButtonGroup


from app.process_api import generate_completed_df

df = generate_completed_df()

p = figure(title="Predictions for Currently Available Notes")


def generate_aggregated_roi(selected_notes):
    """
    Generates the aggregated ROI of

    :return:
    """


output_server("")

# Set Constants
axis_map = {'Estimated ROI': 'estimated_roi', 'Estimated Default %': 'default_prob',
            'Loan Amount': 'loan_amnt', 'Interest Rate': 'int_rate',
            'Installment': 'installment', 'Revolving Balance': 'revol_bal',
            'Annual Income': 'annual_inc', 'Earliest Credit': 'earliest_cr_line',
            'FICO': 'fico', 'Payments / Income': 'payments_to_income'
            }

assert [i in df.columns  for i in axis_map.values()]
grades = list('ABCDEFG')

# Create Controls
minimum_roi = Slider(title="Minimum Estimated Return on Investment", value=.1, start=0.00,
                     end=.25, step=0.01)

max_default = Slider(title="Maximum Default Rate", value=.15, start=0.35, end=0.02, step=-.01)
min_income = Slider(title="Minimum Annual Income (thousands)", value=50, start=0, end=200,
                    step=1)

grades =
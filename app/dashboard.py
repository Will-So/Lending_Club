"""
Steps:
    1. Generate DF and predictions
    2. Display the App

    # Informationa bout selected items
    http://stackoverflow.com/questions/27856348/bokeh-get-information-about-points-that-have-been-selected
"""
import sys
sys.path.append('..')
from app.process_api import generate_completed_df

from bokeh.plotting import Figure
from bokeh.models.widgets import Slider, Select
from bokeh.models import HoverTool, ColumnDataSource, HBox, VBoxForm, Axis
from bokeh.io import curdoc


df = generate_completed_df()

# Truncate very extreme values
df.annual_inc = df.annual_inc.clip(lower=0, upper=200000)

# Set Constants
axis_map = {'Expected ROI': 'estimated_roi', 'Estimated Default %': 'default_prob',
            'Loan Amount': 'loan_amnt', 'Interest Rate': 'int_rate',
            'Installment': 'installment', 'Revolving Balance': 'revol_bal',
            'Annual Income': 'annual_inc', 'Earliest Credit': 'earliest_cr_line',
            'FICO': 'fico', 'Payments / Income': 'payments_to_income'
            }

assert [i in df.columns  for i in axis_map.values()] # Check tomake sure all values are valid

# Create Controls
minimum_roi = Slider(title="Minimum Estimated Return on Investment", value=.1, start=0.00,
                     end=.25, step=0.01)

max_default = Slider(title="Maximum Default Rate", value=.35, start=0.02, end=0.35, step=.01)
min_income = Slider(title="Minimum Annual Income (thousands)", value=50, start=0, end=200,
                    step=1)

max_payments_to_income = Slider(title='Maximum Payments/Income Ratio', value=.40,
                            start=0.00, end=0.40, step=0.01)

x_axis = Select(title="X Axis", options=sorted(axis_map.keys()), value='Annual Income')
y_axis = Select(title='Y Axis', options=sorted(axis_map.keys()), value='Expected ROI')


# Create Column Data Source that will be used by the plot
source = ColumnDataSource(data=dict(x=[], y=[], color=[], title=[], year=[], revenue=[]))

hover = HoverTool(tooltips=[('Interest Rate', '@interest_rate%'),
                            ('Payments / Income', '@payments_to_income%'),
                            ('FICO', '@fico')
                            ])

p = Figure(plot_height=600, plot_width=800, title='', toolbar_location=None, tools=[hover])
p.circle(x='x', y='y', source=source, size=7, color='blue', line_color=None, alpha=0.8)

# Remove scientific notation
yaxis = p.select(dict(type=Axis, layout='left'))[0]
yaxis.formatter.use_scientific = False

p.xaxis[0].formatter = yaxis.formatter


def select_notes():
    """
    Filters the dataframe into notes that satisfy all constraints in web app
    """
    selected = df[
        (df.annual_inc >= min_income.value * 1000) &
        (df.default_prob <= max_default.value) &
        (df.estimated_roi >= minimum_roi.value) &
        (df.payments_to_income <= max_payments_to_income.value)
    ]

    return selected


def update(attrname, old, new):
    """
    Updates the plot according to the criteria

    """
    selected = select_notes()
    x_name = axis_map[x_axis.value]
    y_name = axis_map[y_axis.value]

    p.xaxis.axis_label = x_axis.value
    p.yaxis.axis_label = y_axis.value
    p.title = '{} notes selected'.format(len(selected))

    # TODO Add more to this
    # Multiple by 100 and change to int for clarity
    source.data = dict(x=selected[x_name], y=selected[y_name],
                       fico=selected['fico'], annual_income=selected.annual_inc.astype(int),
                       payments_to_income=(selected.payments_to_income * 100).astype(int),
                       interest_rate=(selected.int_rate * 100).astype(int))

controls = [min_income, max_default, minimum_roi, max_payments_to_income, y_axis, x_axis]
for control in controls:
    control.on_change('value', update)

inputs = HBox(VBoxForm(*controls), width=300)

update(None, None, None)

curdoc().add_root(HBox(inputs, p, width=1100))
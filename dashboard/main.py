"""
Steps:
    1. Generate DF and predictions
    2. Display the App

    # Informationa bout selected items
    http://stackoverflow.com/questions/27856348/bokeh-get-information-about-points-that-have-been-selected
"""
from bokeh.plotting import Figure, show, output_server

from bokeh.models.widgets import Slider, Select, TextInput, CheckboxButtonGroup
from bokeh.models import HoverTool, ColumnDataSource


from app.process_api import generate_completed_df

df = generate_completed_df()

# p = figure(title="Predictions for Currently Available Notes")


def generate_aggregated_roi(selected_notes):
    """
    Generates the aggregated ROI of the selected notes

    :return:
    """


output_server("")

# Set Constants
axis_map = {'Expected ROI': 'estimated_roi', 'Estimated Default %': 'default_prob',
            'Loan Amount': 'loan_amnt', 'Interest Rate': 'int_rate',
            'Installment': 'installment', 'Revolving Balance': 'revol_bal',
            'Annual Income': 'annual_inc', 'Earliest Credit': 'earliest_cr_line',
            'FICO': 'fico', 'Payments / Income': 'payments_to_income'
            }

assert [i in df.columns  for i in axis_map.values()] # Check tomake sure all values are valid
grades = list('ABCDEFG')

# Create Controls
minimum_roi = Slider(title="Minimum Estimated Return on Investment", value=.1, start=0.00,
                     end=.25, step=0.01)

max_default = Slider(title="Maximum Default Rate", value=.15, start=0.35, end=0.02, step=-.01)
min_income = Slider(title="Minimum Annual Income (thousands)", value=50, start=0, end=200,
                    step=1)

grades = CheckboxButtonGroup(labels=grades, active=[0, 1])

x_axis = Select(title="X Axis", options=sorted(axis_map.keys()), value='Expected ROI')
y_axis = Select(title='Y Axis', options=sorted(axis_map.keys()), value='Estimated Default %')


# Create Column Data Source that will be used by the plot
source = ColumnDataSource(data=dict(x=[], y=[], color=[], title=[], year=[], revenue=[]))

hover = HoverTool(tooltips=[('Interest Rate', '@int_rate'),
                            ('Payments / Income', '@payments_to_income'),
                            ('FICO', '@fico')
                            ])

p = Figure(plot_height=800, plot_width=1000, title='', toolbar_location=None, tools=[hover])
p.circle(x='x', y='y', source=source, size=7, color='color', line_color=None, fill_alpha='alpha')


def select_notes():
    """
    TODO: Still need to include grade
    """
    grade_val = grades.value
    selected = df[
        (df.annual_inc >= min_income.value * 1000) &
        (df.default_prob <= max_default.value) &
        (df.estimated_roi >= minimum_roi.value) &
    ]

    return selected


def update(attrname, old, new):
    """

    :param attrname:
    :param old:
    :param new:
    :return:
    """
    selected = select_notes()
    x_name = axis_map[x_axis.value]
    y_name = axis_map[y_axis.value]

    p.xaxis.axis_label = x_axis.value
    p.yaxis.axis_label = y_axis.value
    p.title = '{} notes selected'.format(len(selected))

    # TODO Add more to this
    source.data = dict(x=selected[x_name], y=selected[y_name],
                       fico=selected['fico'])
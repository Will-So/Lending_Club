"""
Steps:
    1. Process the API
    2. Render The table of most beloved Notes
    3. Programaticically place orders

TOOD:
    1. Load the dataframe on starting the web server
    2. Make the HTML template alright

http://stackoverflow.com/questions/22180993/pandas-dataframe-display-on-a-webpage

{% extends "base.html" %}
{% block content %}
<h1>{{name}}</h1>
{{data | safe}}
{% endblock %}
"""
import os
import pandas as pd

from flask import Flask, render_template, request
from execute_orders import roi_floor

from process_api import generate_completed_df

app = Flask(__name__)

df = generate_completed_df()
df_html =  df.to_html().replace('class="dataframe"',
                                   'class="table table-striped table-bordered table-condensed')

loans_available = 0
estimated_roi = 0
last_checked = 0
last_submitted = 0


@app.route('/')
def dashboard():
    return render_template('dashboard.html', roi_floor=roi_floor,
                           loans_available=loans_available,
                           estimated_roi=estimated_roi,
                           last_checked=last_checked,
                           last_submitted=last_submitted)


@app.route('/notes')
def notes():
    """
    The
    :return:
    """

    # TODO: Filter unimportant columns here.

    return render_template('table.html', data=df_html)


@app.route('/log')
def log():
    pass


@app.route('/vis')
def vis():
    pass







    return df_html
if __name__ == '__main__':
    app.run(debug=True)

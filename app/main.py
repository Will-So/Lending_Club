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

from process_api import generate_completed_df

app = Flask(__name__)

# @app.app_context_context_processor
# def inject_df():
#     df = generate_completed_df() ## Not sure how this is supposed to work


# @app.context_processor
# def generate_df():
#     return dict(df=generate_completed_df().to_html())

@app.route('/')
def notes():
    df = pd.read_pickle('../cleaned_df.pkl')[:20]
    return render_template('table.html', data=df.to_html())


if __name__ == '__main__':
    app.run(debug=True)

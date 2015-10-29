"""
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
import requests
import pandas as pd
import sys

from flask import Flask, render_template, request



app = Flask(__name__)

@app.route('/notes')
def notes(df):
    return render_template('notes.html', data=df.to_html())




if __name__ == '__main__':
    app.run(debug=True)
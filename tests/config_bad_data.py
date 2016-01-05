"""
Appends bad data that has tripped up my algorithm before.
"""
import pandas as pd

df = pd.read_csv('good_data.csv')

# Have some categories be missing.
df = df[df.purpose != 'credit_card']
df = df[df.home_ownership != 'RENT']
df = df[df.grade != 'A']

# Populate with 0 values
df.annual_inc.iloc[[2,3,45,12]] = 0

pd.to_csv('bad_data.csv')
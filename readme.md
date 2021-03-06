# Lending Club Optimizer
Predicts the default rate of loans and automatically order the model's favorite currently available loans. Likely to increase ROI from
7.5% (Lending Club Average) to 13.5%. This project identifies investment stratagies that fit custom investment profiles. The user specifies the amount of capital she is willing 
to invest and either her desired expected return or her maximum risk tolerance. 

# Overview
 - The `app` directory has two major entry points.
    - `execute_orders.py` will order the model's favorite loans. `process_api` supports this process. 
    - `main.py` renders a webpage that allows the user to view currently available loans and its expected rate of return.
 
![](https://dl.dropboxusercontent.com/u/97258109/Screens/S3616.png)

- `scripts` contains code used in developing the model
- `notebooks` contains Jupyter Notebooks that tell a story of the process I followed

# Replication

## Getting the data
The full data is available to Lending Club members. The data can be downloaded [here](). **It is critical to first log in as FICO scores are only available once logged in.** 

## Access to the Lending Club API
You need to be registered on the Lending Club site in order to use the lending club API. I recommend that you store the API credentials as an environemntal variable for security reasons. 
My app expects the name of the environmental variable to be `LENDING_CLUB_API`.


# Starting the dashboard app
bokeh serve --show app

# Notes on relative imports
It seems like it is going to be a better idea to handle things

# Restructuring this app
The API here was somewhat ill-planned. This should be turned into a library that accesses multiple things and has a nice API that will
perform various operations (orders, show current notes, and

# Refresh TImes
 2AM, 6AM, 10AM and 2 PM
# Lending Club Optimizer
Predicts the default rate of loans and automatically order the model's favorite currently available loans. Likely to increase ROI from
7.5% (Lending Club Average) to 13.5%. This project identifies investment stratagies that fit custom investment profiles. The user specifies the amount of capital she is willing 
to invest and either her desired expected return or her maximum risk tolerance. 

# Overview
//todo make into bullet points
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

# Methodology

# Lessons Learned
1. Write down a basic example of the tool before I actually get started with the thing. Starting with something complicated is bound to fail even if you think the thing is going to work alright.
4. Never assume that API data will be in the same format as the historical data. 
4. Put the data into its own directory. I didn't forese at the beginning that this project would **generate** so much 
data but this is what ended up happening:
![](https://dl.dropboxusercontent.com/u/97258109/Screens/S3584.png)


# Lending Club Optimizer
Predicts the default rate of loans and automatically order the model's favorite currently available loans. Likely to increase ROI from
7.5% (Lending Club Average) to 13.5%. This project identifies investment stratagies that fit custom investment profiles. The user specifies the amount of capital she is willing 
to invest and either her desired expected return or her maximum risk tolerance. 

# Overview
The `app` directory has two major entry points. `execute_orders.py` will order the model's favorite loans. `main.py`
renders a webpage that allows the user to view currently available loans and its expected rate of return.

![](https://dl.dropboxusercontent.com/u/97258109/Screens/S3585.png)

The `scripts` directory provides some code used in training the model as well as the data necessary to clean the historical data. `notebooks` provides some rough drafts of what
I did to make this code as well as some other models I used. 

# Replication

## Getting the data
The full data is available to Lending Club members. The data can be downloaded [here](). **It is critical to first log in as FICO scores are only available once logged in.** 

## Access to the Lending Club API
You need to be registered on the Lending Club site in order to use the lending club API. I recommend that you store the API credentials as an environemntal variable for security reasons. 
My app expects the name of the environmental variable to be `LENDING_CLUB_API`.

# Methodology

## Steps Taken
For this first iteration, I have taken the following steps:
1. Clean the data (`clean_data.py`)
2. Try some models that are easy and fast to tune; evaluate performance. (`model.py` and (especially)
 `modeling.ipynb`). Pick the best one.
3. Build a pipeline that collects loans currently in funding and cleans it (`process_api.py`).
4. Make a super simple web app that displays the loans that are currently availble to invest in along with their expected default and ROI
5. Make a script that will order the model's favorite loans. Make a cron job that runs it 4x daily. Forget until I need money. 


## Removing Certain Data Points
1. I only consider notes that are more than a year old. Younger note performance is not likely to be indicative of longer-term returns.
2. I removed entries that did not meet Lending Clubs revised lending standard (~2000 loans between 2007-2010) because they don't generalize. 
3. Return rate is calculated via $int\_rate * (1 - p(default)) + p(default) * (1- recovery\_if\_default)$ // Double check to make sure that this equation is accurate
4. $recovery\_if\_default$ is calculated as being the mean recovery percentage. 

## Notes on Modeling
- Excluding risky loans seems to improve the reliability of the model for riskier loans.
    - See `modeling.ipynb` for the intuition why this should be the case.
- I engineered the model's second most predictive feature, the estimated ratio of total monthly debt payments (credit cards + future
Lending Club loan) to income. 
- The model think's lending club does a very good job deciding who to lend to. 

# Lessons Learned
1. Write down a basic example of the tool before I actually get started with the thing. Starting with something complicated is bound to fail even if you think the thing is going to work alright.
4. Never assume that API data will be in the same format as the historical data. 
4. Put the data into its own directory. I didn't forese at the beginning that this project would **generate** so much 
data but this is what ended up happening:
![](https://dl.dropboxusercontent.com/u/97258109/Screens/S3584.png)

# General Thoughts on Modeling Risk
1. Have a Great Recession model that shows how the lending club notes return would change based on everything else. 
2. Matching might be a good strategy as well. KNN 


# Bankrupty Problem
Diversifying loans 

1. Probably alright but small chance that Federal Bankruptcy court eliminates all contracts
2. Have replacement bank in place
3. Prosper is 100% protected via a [cool idea]()

# Iteration Number 2
1. Make the Web App much better
    - Integrate with Tableau Dashboard
2. Try some more ML models to see what the best results will be
    - Especially gradienting boostinggit 
3. Clean up the HTML files so that they work better
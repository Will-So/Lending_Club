# Lending Club Optimizer

This package identifies investment stratagies that fit custom investment profiles. The user specifies the amount of capital she is willing to invest and either her desired expected return or her maximum risk tolerance. 

This project also includes a script, `execute_orders.py` that will order the model's favorite loans 


# Replication

## Getting the data
The full data is available to Lending Club members. The data can be downloaded [here](). **It is critical to first log in as FICO scores are only available once logged in.** 

## The scripts
The most important scripts are:
You can run the `clean_data.py` script immediately to get the data into both csv and pickle formats. After that `model.py` will train the model. 

Altera

https://github.com/ThinkBigAnalytics/stampede/wiki/Make-and-Bash-Tips

## The Notebooks
At this time, notebooks are only scratch notes. 

## Access to the Lending Club API
You need to be registered on the Lending Club site in order to use the lending club API. I recommend that you store the API credentials as an environemntal variable for security reasons. 


# Methodology

## Steps Taken
For this first iteration, I have taken the following steps:
1. Clean the data (`clean_data.py`)
2. Try some models that are easy and fast to tune; evaluate performance. (`model.py` and (especially)
 `modeling.ipynb`. Pick the best one. 
3. 


## Removing Certain Data Points
1. I only consider notes that are more than a year old. Younger note performance is not likely to be indicative of longer-term returns.
2. I removed entries that did not meet Lending Clubs revised lending standard (~2000 loans between 2007-2010) because they don't generalize. 
3. Return rate is calculated via $int\_rate * (1 - p(default)) + p(default) * (1- recovery\_if\_default)$ // Double check to make sure that this equation is accurate
4. $recovery\_if\_default$ is calculated as being the mean recovery percentage. 
5. 

## Notes on Modeling
- Excluding risky loans seems to improve the reliability of the model for riskier loans.
    - See `modeling.ipynb` for the intuition why this should be the case.

# UI
The users specifies how much capital they are looking to invest and either a minimum level of returns or a maximum level of downside risk. The application then returns 

Screenshots can be found [here](). 


# Lessons Learned
1. Write down a basic example of the tool before I actually get started with the thing. Starting with something complicated is bound to fail even if you think the thing is going to work alright.
2. Read the documentation more `predict_proba(X)` is a nice touch that should have worked a bit better. This is also enabling us to get our thresholds better.
4. Never assume that dealing with someone else's data is going to be trivially easy even if you have been having a great experience with them previously.
4. Put the data into its own directory as well. I didn't forese at the beginning that this project would **generate** so much 
data but that is what ended up happening
5. 


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
    - 
2. Try some more ML models to see what the best results will be
    - Especially gradienting boostinggit 
3. Clean up the HTML files so that they work better
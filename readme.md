# Lending Club Optimizer

This package identifies investment stratagies that fit custom investment profiles. The user specifies the amount of capital she is willing to invest and either her desired expected return or her maximum risk tolerance. 


# Replication

## Getting the data
The full data is available to Lending Club members. The data can be downloaded [here](). **It is critical that you log in first as FICO scores are only available once logged in.**

## The scripts
You can run the `clean_data.py` script immediately to get the data into both csv and pickle formats. After that `model.py` will train the model. 

Altera

https://github.com/ThinkBigAnalytics/stampede/wiki/Make-and-Bash-Tips

## Access to the Lending Club API
You need to be registered on the Lending Club site in order to use the lending club API. I recommend that you store the API credentials as an environemntal variable for security reasons. 


# Methodology
## Removing Certain Data Points
1. I only consider notes that are more than a year old. Younger note performance is not likely to be indicative of longer-term returns.
2. I removed entries that did not meet Lending Clubs revised lending standard (~2000 loans between 2007-2010) because they don't generalize. 
3. Return rate is calculated via $int\_rate * (1 - p(default)) + (1 - p(default)) * (1- recovery\_if\_default)$ //This part of the formula is wrong
4. $recovery\_if\_default$ is calculated as being the mean recovery percentage. 
5. 

# UI
The users specifies how much capital they are looking to invest and either a minimum level of returns or a maximum level of downside risk. The application then returns 

Screenshots can be found [here](). 


# Lessons Learned
1. Write down a basic example of the tool before I actually get started with the thing. Starting with something complicated is bound to fail even if you think the thing is going to work alright.
2. Read the documentaiton more `predict_proba(X)` is a nice touch that should have worked a bit better. This is also enabling us to get our thresholds better.


# General Thoughts on Modeling Risk
1. Have a Great Recession model that shows how the lending club notes return would change based on everything else. 
2. Matching might be a good strategy as well. KNN 


# Bankrupty Problems
1. Probably alright but small chance that Federal Bankruptcy court eliminates all contracts
2. Have replacement bank in place
3. Prosper is 100% protected via a [cool idea]()
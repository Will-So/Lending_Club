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

# General Thoughts on Modeling Risk
1. Have a Great Recession model that shows how the lending club notes return would change based on everything else. 
2. Matching might be a good strategy as well. KNN 

"""
Creates all of the necessary steps for our mode.

1. Trains a model
2. Predicts the default rate given a model
3. Predicts payment received in the case of default
4. Predicts total ROI
"""

from patsy import dmatrices
import sys
import pandas as pd
from sklearn.linear_model import LogisticRegressionCV
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier
import numpy as np


def _main():
    df = pd.read_pickle('../cleaned_df.pkl')
    y, X = create_matrix(df)
    train_X, test_X, train_y, test_y = train_test_split(X, y, test_size=0.8)
    fitted_model = fit_random_forest(train_X, train_y)
    default_recovery = percent_paid_if_default(df)


def create_matrix(df):
    """
    Creates a matrix of dummies
    :param df: cleaned pd.DataFrame()
    :return: y: Vector of targets ; X: vector of features
    """
    y, X = dmatrices('delinq ~  + loan_amnt + int_rate + installment + emp_length +'
                 'C(home_ownership) + C(grade) + C(purpose) + C(addr_state) + '
                 'inq_last_6mths + pub_rec + revol_bal +open_acc + collections_12_mths_ex_med'
                 ' + delinq_2yrs + earliest_cr_line  + fico_range_low + ratio_mth_inc_all_payments + annual_inc',
                 df, return_type='dataframe', NA_action='drop')

    y = np.ravel(y)
    return y, X


def fit_logistic_regression(y, X):
    """
    Fites a logistic regression
    """
    model_log = LogisticRegressionCV(cv=5, penalty='l2', verbose=1, max_iter=1000)
    fit = model_log.fit(X, y)

    return fit


def fit_random_forest(y, X):
    """
    Fits a random forest
    """
    model_rf = RandomForestClassifier(n_estimators=200, oob_score=True, verbose=1, random_state=2143,
                                      min_samples_split=50)
    fitted_model = model_rf.fit(X, y)

    return fitted_model


def percent_paid_if_default(df):
    """
    returns the percentage paid in case of default.

    """
    default_df = df.assign(percentage_paid= df.total_pymnt/df.loan_amnt
                      )[df.loan_status=='Charged Off']
    return default_df.percentage_paid.mean()

# Generate Confusion Matrix
# SVM



if __name__ == '__main__':
    sys.exit(_main())
from patsy import dmatrices
import sys
import pandas as pd
from sklearn.linear_model import LogisticRegressionCV
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier




def _main():
    df = pd.read_pickle('../cleaned_df.pkl')
    y, X = create_matrix(df)
    train_X, test_X, train_y, test_y = train_test_split(X, y, test_size=0.8)



def create_matrix(df):
    """
    Creates a matrix of dummies
    :param df: df from cleaned
    :return:
    """
    y, X = dmatrices('delinq ~ C(zip_code) + loan_amnt*int_rate + installment + emp_length +'
                     'C(home_ownership) + C(grade) + sub_grade + C(month_issued) + C(year_issued)'
                     '+ C(purpose) + C(addr_state) + inq_last_6mths + pub_rec + revol_bal +open_acc+'
                     'collections_12_mths_ex_med + delinq_2yrs + earliest_cr_line + fico_range_low'
                     '+ ratio_mth_inc_all_payments',
                     df, return_type='dataframe')
    return y, X


def fit_logistic_regression(y, X):
    """

    :param y:
    :param X:
    :return:
    """
    model_log = LogisticRegressionCV(cv=5, penalty='l2', verbose=1, max_iter=1000)
    fit = model_log.fit(X, y)



def fit_random_forest(y, X):
    """

    :param y:
    :param X:
    :return:
    """
    model_rf = RandomForestClassifier(n_estimators=50, oob_score=True, verbose=1, random_state=2143,
                                      min_samples_split=50)
    fitted_model = model_rf.fit(X, y)





if __name__ == '__main__':
    sys.exit(_main())
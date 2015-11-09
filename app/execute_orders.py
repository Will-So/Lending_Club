"""
CLI that is meant to run in the background and place orders hourly.

Look into celery for doing this.

TODO:
    - Set up multi-user functionality. Need to use it for 4 accounts eventually.
    - Have it be a CLI that will give the user name and then do everything else and set up logging in each case
    - Change debug to be module wide
"""

from process_api import generate_completed_df
import sqlite3
import sys
import arrow
import time
import requests
import os
import logging

# Set Order Settings
roi_floor = .10
default_floor = .20
amount = 25

# init db
conn = sqlite3.connect('../lc.sqlite')
c = conn.cursor()

# Set Lending Club variables
credentials = os.environ['LENDING_CLUB_API']
headers = {'Authorization': credentials}
investor_id = 5809260
portfolio_id = 65013027

# Init Logging
logging.basicConfig(filename='../orders.log',level=logging.DEBUG)
logging.getLogger("requests").setLevel(logging.WARNING)

# TODO: Verify that logging is working and then remove print statements
# TODO: Verify that


def has_enough_cash():
    """

    :return:
    """
    r = requests.get('https://api.lendingclub.com/api/investor/v1/accounts/{}/availablecash'.format(investor_id),
                    headers=headers)

    cash = r.json()['availableCash']
    return True if cash > 25 else False


def _main():
    """
    Predicts which loans will perform the best and then places orders on those if
    there is enough cash and if the loan has not already been ordered.

    """
    df = generate_completed_df()
    good_ids = df.id[(df.estimated_roi > roi_floor) & (df.default_prob < default_floor)]

    already_ordered = []
    for row in c.execute('SELECT * FROM orders'):
        already_ordered.append(row[1])

    print("Placing orders for {} loans \n{} already ordered"
            .format(len(set((good_ids)) - set(already_ordered)), len(already_ordered)))

    for id in good_ids:
        if id not in already_ordered and has_enough_cash():
             place_order(id)
        elif not has_enough_cash():
            print("No cash left")
            logging.debug("No Cash left")
            break

    logging.debug("Finished Ordering")
    print("Finished ordering")


def place_order(id):
    """
    Places an order and appends the ordered loan

    """

    print("Test Submitting Order for {}".format(id))
    logging.debug("Submitting Order for {}".format(id))
    now = arrow.utcnow().format('YYYY-MM-DDTHH:mm:ss')

    payload = {"aid": '{}'.format(investor_id),
               "orders": [
             {
                "loanId": '{}'.format(int(id)),
                "requestedAmount": '{}'.format(amount),
                "portfolioId": '{}'.format(portfolio_id)
                }
                ]}

    print(payload)
    logging.debug("This is the payload sent: {}".format(payload))

    r = requests.post('https://api.lendingclub.com/api/investor/v1/accounts/{}/orders'
                      .format(investor_id), json=payload,
                      headers= headers)

    print(r.status_code)
    print(r.text)
    
    if r.status_code == 200:
        c.execute("""INSERT INTO orders VALUES ("{0}", {1}, {2})"""
                    .format(now, id, amount))
        conn.commit()
        
        logging.debug("Text for id {} : {} at {}".format(id, r.text, now))
    else:
        logging.debug("Order for id {} failed. {} at {}".format(id, r.status_code, now))

    time.sleep(1)


# def place_order():
#     """
#     Will refactor place_order and generate_order in two different functions for debugging purposes

#     :return:
#     """


def init_db():
    conn = sqlite3.connect('lc.sqlite')
    c = conn.cursor()
    c.execute('''CREATE TABLE orders (date text, id INTEGER PRIMARY KEY, amount REAL) ''')
    conn.commit()
    conn.close()


if __name__ == '__main__':
    sys.exit(_main())

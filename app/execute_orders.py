"""
CLI that is meant to run in the background and place orders hourly.

Look into celery for doing this.

TODO:
    - Set up multi-user functionality. Need to use it for 4 accounts eventually.
    - Have it be a CLI that will give the user name and then do everything else and set up logging in each case
    - Change debug to be module wide
    - Add a cash reserves option
"""

import sqlite3
import sys
import arrow
import time
import requests
import os
import logging

sys.path.append('..')
from process_api import generate_completed_df


# Set Order Settings
roi_floor = .10
default_floor = .20
amount = 25
cash_reserves = 0 # Desired level of cash balance

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
logging.getLogger('werkzeug').setLevel(logging.WARNING)


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

    logging.debug("Placing orders for {} loans \n{} already ordered"
            .format(len(set((good_ids)) - set(already_ordered)), len(already_ordered)))

    for id in good_ids:
        funds_available = has_enough_cash() # Called once to avoid dirty logs
        if id not in already_ordered and funds_available:
             place_order(id)
        elif not funds_available:
            logging.debug("No Cash left")
            break

    logging.debug("Finished Ordering")


def place_order(id):
    """
    Generates the order payload and places an order and appends the ordered loan
    """
    now = arrow.utcnow().format('YYYY-MM-DDTHH:mm:ss')
    logging.debug("Submitting Order for {} at {}".format(id, now))

    payload = {"aid": '{}'.format(investor_id),
               "orders": [
             {
                "loanId": '{}'.format(int(id)),
                "requestedAmount": '{}'.format(amount),
                "portfolioId": '{}'.format(portfolio_id)
                }
                ]}

    logging.debug("This is the payload sent: {}".format(payload))

    r = requests.post('https://api.lendingclub.com/api/investor/v1/accounts/{}/orders'
                      .format(investor_id), json=payload, headers= headers)

    if r.status_code == 200:
        c.execute("""INSERT INTO orders VALUES ("{0}", {1}, {2})"""
                    .format(now, id, amount))
        conn.commit()
        
        logging.debug("SUCCESS: for id {} : {} at {} successful".format(id, r.text, now))
    else:
        logging.debug("Order for id {} failed. {} at {}".format(id, r.status_code, now))

    time.sleep(1)


def has_enough_cash():
    """
    Checks if I currently have money in my lending club account.
    """
    r = requests.get('https://api.lendingclub.com/api/investor/v1/accounts/{}/availablecash'
                     .format(investor_id), headers=headers)

    cash = r.json()['availableCash']
    logging.debug(cash)
    return True if cash > cash_reserves + amount else False


# TODO: Get this into a general setup script.
def init_db():
    """
    Initializes a SQL database that keeps track of documents already odered.

    Only needs to be run on initial setup
    """
    conn = sqlite3.connect('lc.sqlite')
    c = conn.cursor()
    c.execute('''CREATE TABLE orders (date text, id INTEGER PRIMARY KEY, amount REAL) ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    sys.exit(_main())

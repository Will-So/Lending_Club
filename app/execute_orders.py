#!/usr/bin/env python3
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
import logging
import os

sys.path.append('..')
import app.config as config
from app.process_api import generate_completed_df

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
print(FILE_DIR)
SQL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
print(SQL_DIR)


# Set Order Settings
roi_floor = .125
default_floor = .20
amount = 50
cash_reserves = 0 # Desired level of cash balance
three_years_only = True

# Connect to db
conn  = sqlite3.connect(os.path.join(SQL_DIR, 'lc.sqlite'))
# conn = sqlite3.connect('../lc.sqlite')
c = conn.cursor()

# Set Lending Club variables
headers = {'Authorization': config.main_config['credentials']}
investor_id = config.main_config['investor_id']
portfolio_id = config.main_config['portfolio_id']

# Init Logging
logging.basicConfig(filename='../orders.log',level=logging.DEBUG,
                    format='%(asctime)s %(message)s')
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger('werkzeug').setLevel(logging.WARNING)


def _main():
    """
    Predicts which loans will perform the best and then places orders on those if
    there is enough cash and if the loan has not already been ordered.
    """
    count = 0
    df = generate_completed_df()
    # import pdb; pdb.set_trace()

    if three_years_only:
        df = df[df.term == 36]

    good_ids = set(df.ix[(df.estimated_roi > roi_floor) &
                     (df.default_prob < default_floor)].index)

    already_ordered = set()
    for row in c.execute('SELECT * FROM orders'):
        already_ordered.add(row[1])

    good_ids = good_ids - already_ordered

    logging.debug("Placing orders for {} loans \n{} already ordered"
            .format(len(set((good_ids)) - set(already_ordered)), len(already_ordered))) # TODO Consider making a new_orders thing with the set.

    order_ids = []
    pending_amount = 0
    for id in good_ids:
        funds_available = has_enough_cash(pending_amount) # Called once to avoid dirty logs
        if id not in already_ordered and funds_available:
            count += 1
            pending_amount += amount
            order_ids.append(id)
        elif not funds_available:
            logging.debug("No Cash left")
            break
        elif id in already_ordered:
            logging.info("{} Was previously ordered".format(id))

    place_order(order_ids)

    logging.debug("Finished Ordering ordered {} notes \n".format(count))


def place_order(good_ids):
    """
    Generates the order payload and places an order and appends the ordered loan
    """
    now = arrow.utcnow().format('YYYY-MM-DDTHH:mm:ss')
    logging.debug("Submitting Order for {} at {}".format(good_ids, now))

    payload = {"aid": '{}'.format(investor_id),
               "orders": [
                   {"loanId": '{}'.format(int(id)),
                    "requestedAmount": '{}'.format(amount),
                    "portfolioId": '{}'.format(portfolio_id)} for id in
                        good_ids
                ]}

    logging.debug("This is the payload sent: {}".format(payload))

    r = requests.post('https://api.lendingclub.com/api/investor/v1/accounts/{}/orders'
                      .format(investor_id), json=payload, headers= headers)

    for id in good_ids:
        if r.status_code == 200:
            c.execute("""INSERT INTO orders VALUES ("{0}", {1}, {2})"""
                    .format(now, id, amount))
            conn.commit()

    if r.status_code == 200:
        logging.debug("SUCCESS: for id {} : {} at {} successful".format(good_ids, r.text, now))
    else:
        logging.debug("Order for id {} failed. {} at {}".format(good_ids, r.status_code, now))

    time.sleep(1)


def has_enough_cash(pending=0):
    """
    Checks if I currently have money in my lending club account.
    """
    r = requests.get('https://api.lendingclub.com/api/investor/v1/accounts/{}/availablecash'
                     .format(investor_id), headers=headers)

    cash = r.json()['availableCash']
    logging.debug(cash - pending)

    return True if cash - pending > cash_reserves + amount else False


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

"""
Logs daily summaries for daily orders. Currently assumes only one account.
"""
## TODO Add current balance.

import sqlite3
import logging
import os
import sys

sys.path.append('..')
from app.execute_orders import has_enough_cash


# Init Logging
logging.basicConfig(filename='~/logs/daily_summary.log',level=logging.DEBUG,
                    format='%(asctime)s %(message)s')

SQL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))


conn  = sqlite3.connect(os.path.join(SQL_DIR, 'lc.sqlite'))
c = conn.cursor()

orders_today = """select count(*) from orders where date(date) = date('now')
"""

orders_today = c.execute(orders_today)

amount_ordered = """select sum(amount) from orders where date(date) = date('now')
"""
amount_ordered = c.execute(amount_ordered)

amount_remaining = has_enough_cash()
logging.info("{} is Remaining".format(amount_ordered))

logging.info("{} orders submitted today".format(orders_today))

logging.info("{}$ amount ordered".format(orders_today))
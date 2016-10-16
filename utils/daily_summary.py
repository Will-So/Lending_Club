"""
Logs daily summaries for daily orders. Currently assumes only one account.
"""
## TODO Add current balance.

import sqlite3
import logging
import os
import sys

sys.path.append('../app')
from execute_orders import amount_remaining

logger = logging.getLogger()
SQL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))


conn  = sqlite3.connect(os.path.join(SQL_DIR, 'lc.sqlite'))
c = conn.cursor()

# import pdb; pdb.set_trace()

orders_today = """select count(*) from orders where date(date) = date('now')"""

orders_today = c.execute(orders_today).fetchall()[0][0] ## 0th item in the tuple of the 0th item of the list

amount_ordered = """select sum(amount) from orders where date(date) = date('now')
"""

amount_ordered = c.execute(amount_ordered).fetchall()[0][0] ## 0th item in the tuple of the 0th item of the list

amount_remaining = amount_remaining()
logger.info("{} is Remaining".format(amount_remaining))

logger.info("{} orders submitted today".format(orders_today))

logger.info("{}$ amount ordered".format(amount_ordered))

print(orders_today, amount_ordered, amount_remaining)
import sqlite3
import arrow

conn = sqlite3.connect('../test_lc.sqlite')
c = conn.cursor()

test_id = 23123213123123213
test_amount = 10000
now = arrow.utcnow().format('')

# TODO: Make a long series of test dataframes


def test_sql_write():
    """

    :return:
    """
    c.execute("""INSERT INTO orders VALUES ("{0}", {1}, {2})""".format(now, test_id, test_amount))
    c.commit()

def test_can_model():
    """

    :return:
    """

def test_no_order_twice():
    """
    Verifies that the same security cannot be ordered twice
    :return:
    """
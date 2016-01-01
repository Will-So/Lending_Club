import sqlite3
import arrow
import pytest

conn = sqlite3.connect('test_lc.sqlite')
c = conn.cursor()

test_id = 23123213123123213
test_amount = 10000
now = arrow.utcnow().format('')

# TODO: Make a long series of test dataframes


def test_sql_write(init_db):
    """

    :return:
    """
    c = conn.cursor()
    c.execute("""INSERT INTO orders VALUES ("{0}", {1}, {2})""".format(now, test_id, test_amount))
    conn.commit()
    c.execute("SELECT * FROM orders")
    print(c.fetchall())



def test_can_model():
    """

    :return:
    """

def test_no_order_twice():
    """
    Verifies that the same security cannot be ordered twice
    :return:
    """


@pytest.fixture(scope='session')
def init_db(request):
    """
    Initializes a SQL database that keeps track of documents already odered.

    Only needs to be run on initial setup
    """
    # conn = sqlite3.connect('test_lc.sqlite')
    # c = conn.cursor()
    c.execute('''CREATE TABLE orders (date text, id INTEGER PRIMARY KEY, amount REAL) ''')
    conn.commit()
    def teardown():
        c.execute('''DROP TABLE orders''')
        conn.close()
    request.addfinalizer(teardown)


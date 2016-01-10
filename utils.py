import requests


def get_portfolio_id(investor_id, header):
    """
    Retrieves portfolio ids
    """
    r = requests.get('https://api.lendingclub.com/api/investor/v1/accounts/{}/portfolios'
                      .format(investor_id), headers=headers)
import requests


def get_portfolio_id(investor_id, headers):
    """
    Retrieves portfolio ids
    :param investor_id: int specifying the id of investor
    :param headers: header to be sent with the request. Usually just the authoriation
    :return: JSON of the request.
    """
    r = requests.get('https://api.lendingclub.com/api/investor/v1/accounts/{}/portfolios'
                      .format(investor_id), headers=headers)

    return r
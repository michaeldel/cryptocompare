import requests


ERROR_TYPE_THRESHOLD = 100


class CryptoCompare(requests.Session):
    def __init__(self, app_name=None):
        self.app_name = None

    def get_price(self, fsym, tsyms):
        url = 'https://min-api.cryptocompare.com/data/price?fsym={}&tsyms={}&extraParams={}'

        if isinstance(tsyms, (list, tuple, set)):
            tsyms = ','.join(tsyms)

        result = requests.get(url.format(fsym.upper(), tsyms.upper(), self.app_name)).json()

        if result.get('Response') == 'Error' or result.get('Type', ERROR_TYPE_THRESHOLD) < ERROR_TYPE_THRESHOLD:
            raise CryptoCompareApiError(result['Message'])
        return result


class CryptoCompareApiError(Exception):
    pass

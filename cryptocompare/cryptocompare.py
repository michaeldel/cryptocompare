import requests


ERROR_TYPE_THRESHOLD = 100


class CryptoCompare(requests.Session):
    def __init__(self, app_name=None):
        self.app_name = None

    def get_price(self, fsym, tsyms):
        url = 'https://min-api.cryptocompare.com/data/price?fsym={fsym}&tsyms={tsyms}{extra_params}'

        if isinstance(tsyms, (list, tuple, set)):
            tsyms = ','.join(tsyms)

        result = requests.get(url.format(
            fsym=fsym.upper(),
            tsyms=tsyms.upper(),
            extra_params='&extraParams='.format(self.app_name) if self.app_name else ''
        )).json()

        if result.get('Response') == 'Error' or result.get('Type', ERROR_TYPE_THRESHOLD) < ERROR_TYPE_THRESHOLD:
            raise CryptoCompareApiError(result['Message'])
        return result


class CryptoCompareApiError(Exception):
    pass

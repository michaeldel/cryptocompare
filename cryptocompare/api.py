import requests


ERROR_TYPE_THRESHOLD = 100


class CryptoCompare(requests.Session):
    def __init__(self, app_name=None):
        self.app_name = None

    @staticmethod
    def _check_request_response_error(response):
        if response.get('Response') == 'Error' or response.get('Type', ERROR_TYPE_THRESHOLD) < ERROR_TYPE_THRESHOLD:
            raise CryptoCompareApiError(response.get('Message'))

    def get_coin_list(self):
        url = 'https://www.cryptocompare.com/api/data/coinlist'
        result = requests.get(url).json()

        self.__class__._check_request_response_error(result)
        return result['Data']

    def get_price(self, fsyms, tsyms, exchange=None):
        url = 'https://min-api.cryptocompare.com/data/pricemulti?fsyms={fsyms}&tsyms={tsyms}{exchange}{extra_params}'

        if isinstance(fsyms, (list, tuple, set)):
            fsyms = ','.join(fsyms)
        if isinstance(tsyms, (list, tuple, set)):
            tsyms = ','.join(tsyms)

        result = requests.get(url.format(
            fsyms=fsyms.upper(),
            tsyms=tsyms.upper(),
            exchange='&e={}'.format(exchange) if exchange else '',
            extra_params='&extraParams={}'.format(self.app_name) if self.app_name else ''
        )).json()

        self.__class__._check_request_response_error(result)
        return result

    def get_mining_contracts(self):
        url = 'https://www.cryptocompare.com/api/data/miningcontracts'
        result = requests.get(url).json()

        self.__class__._check_request_response_error(result)
        return result['MiningData']

    def get_mining_equipement(self):
        url = 'https://www.cryptocompare.com/api/data/miningequipment'
        result = requests.get(url).json()

        self.__class__._check_request_response_error(result)
        return result['MiningData']


class CryptoCompareApiError(Exception):
    pass

import requests


ERROR_TYPE_THRESHOLD = 100


class CryptoCompare(requests.Session):
    def __init__(self, app_name=None):
        self.app_name = None

    @staticmethod
    def _check_request_response_error(response):
        if not isinstance(response, dict):
            return
        if response.get('Response') == 'Error' or response.get('Type', ERROR_TYPE_THRESHOLD) < ERROR_TYPE_THRESHOLD:
            raise CryptoCompareApiError(response.get('Message'))

    def get_coin_list(self):
        url = 'https://min-api.cryptocompare.com/data/all/coinlist'
        result = requests.get(url).json()

        self.__class__._check_request_response_error(result)
        return result['Data']

    def get_exchange_list(self):
        url = 'https://min-api.cryptocompare.com/data/all/exchanges'
        result = requests.get(url).json()

        self.__class__._check_request_response_error(result)
        return result

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

    def get_coin_snapshot(self, fsym, tsym):
        url = 'https://www.cryptocompare.com/api/data/coinsnapshot/?fsym={fsym}&tsym={tsym}'
        result = requests.get(url.format(tsym=tsym, fsym=fsym)).json()

        self.__class__._check_request_response_error(result)
        return result['Data']

    def get_coin_snapshot_full_by_id(self, coin_id):
        url = 'https://www.cryptocompare.com/api/data/coinsnapshotfullbyid/?id={id}'
        result = requests.get(url.format(id=coin_id)).json()

        self.__class__._check_request_response_error(result)
        return result['Data']

    def get_social_stats(self, coin_id):
        url = 'https://www.cryptocompare.com/api/data/socialstats/?id={id}'
        result = requests.get(url.format(id=coin_id)).json()

        self.__class__._check_request_response_error(result)
        return result['Data']

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

    def get_top_pairs(self, fsym, limit=None):
        url = 'https://min-api.cryptocompare.com/data/top/pairs?fsym={fsym}{limit}{extra_params}'
        result = requests.get(url.format(
            fsym=fsym.upper(),
            limit='&limit={}'.format(limit) if limit else '',
            extra_params='&extraParams={}'.format(self.app_name) if self.app_name else ''
        )).json()

        self.__class__._check_request_response_error(result)
        return result['Data']

    def get_news_providers(self):
        url = 'https://min-api.cryptocompare.com/data/news/providers?{extra_params}'
        return requests.get(url.format(
            extra_params='&extraParams={}'.format(self.app_name) if self.app_name else ''
        )).json()


class CryptoCompareApiError(Exception):
    pass

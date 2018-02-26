import unittest

from cryptocompare import CryptoCompare, CryptoCompareApiError


class TestGetPrice(unittest.TestCase):
    def test_bitcoin_usd(self):
        """Request BTC/USD price should return that pair rate"""
        cc = CryptoCompare()
        result = cc.get_price('BTC', 'USD')
        self.assertIsInstance(result['USD'], float)

    def test_immaginary_pair(self):
        """Requesting price for a pair that do not exist should fail"""
        cc = CryptoCompare()
        self.assertRaises(
            CryptoCompareApiError, cc.get_price, 'LOREMIPSUM', 'DOLORSITAMET'
        )

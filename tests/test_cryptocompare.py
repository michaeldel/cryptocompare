import numbers
import unittest

from cryptocompare import CryptoCompare, CryptoCompareApiError


class TestGetPrice(unittest.TestCase):
    def test_bitcoin_usd(self):
        """Request BTC/USD price should return that pair rate"""
        cc = CryptoCompare()
        result = cc.get_price('BTC', 'USD')
        self.assertIsInstance(result['BTC']['USD'], numbers.Real)

    def test_bitcoin_multiple_tsyms(self):
        """Requesting multiple price for multiple quote symbols should work"""
        cc = CryptoCompare()
        tsyms = ['USD', 'EUR', 'JPY', 'ETH']
        result = cc.get_price('BTC', tsyms)
        for symbol in tsyms:
            self.assertIn(symbol, result['BTC'].keys())

    def test_multiple_fsyms_and_tsyms(self):
        """Requesting multiple price for multiple base and quote symbols should work"""
        cc = CryptoCompare()
        fsyms = ['BTC', 'LTC', 'ETH']
        tsyms = ['USD', 'EUR']
        result = cc.get_price(fsyms, tsyms)
        for fs in fsyms:
            for ts in tsyms:
                self.assertIn(ts, result[fs])

    def test_bitcoin_lowercase(self):
        """Working with lowercase symbols should work"""
        cc = CryptoCompare()
        result = cc.get_price('btc', 'usd')
        self.assertIsInstance(result['BTC']['USD'], numbers.Real)

    def test_unknown_pair(self):
        """Requesting price for a pair that does not exist should fail"""
        cc = CryptoCompare()
        self.assertRaises(
            CryptoCompareApiError, cc.get_price, 'LOREMIPSUM', 'DOLORSITAMET'
        )

    def test_bitcoin_usd_specific_exchange(self):
        """Request BTC/USD price on specific exchange should work"""
        cc = CryptoCompare()
        result = cc.get_price('BTC', 'USD', exchange='Bitstamp')
        self.assertIsInstance(result['BTC']['USD'], numbers.Real)

    def test_bitcoin_usd_specific_unknown_exchange(self):
        """Requesting price for a pair on an exchange that does not exist should fail"""
        cc = CryptoCompare()
        self.assertRaises(
            CryptoCompareApiError, cc.get_price, 'BTC', 'USD', exchange='foo'
        )

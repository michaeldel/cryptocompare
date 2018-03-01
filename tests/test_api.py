import numbers
import unittest

from cryptocompare import CryptoCompare, CryptoCompareApiError, ERROR_TYPE_THRESHOLD

BTC_ID = 1182


class TestCheckRequestResponseError(unittest.TestCase):
    def test_empty(self):
        """Empty response should not raise error"""
        CryptoCompare._check_request_response_error({})

    def test_data(self):
        """Regular response data should not raise error"""
        CryptoCompare._check_request_response_error({'a': 'b'})

    def test_explicit_error_response(self):
        """Response containing error message should raise error"""
        self.assertRaises(
            CryptoCompareApiError,
            CryptoCompare._check_request_response_error,
            {'Response': 'Error'}
        )

    def test_type_under_threshold(self):
        """
        Response containing type field under CryptoCompare threshold should raise error
        """
        self.assertRaises(
            CryptoCompareApiError,
            CryptoCompare._check_request_response_error,
            {'Type': ERROR_TYPE_THRESHOLD - 1}
        )

    def test_type_equal_orover_threshold(self):
        """
        Response containing type field equal to or over CryptoCompare threshold
        should not raise any error
        """
        CryptoCompare._check_request_response_error({'Type': ERROR_TYPE_THRESHOLD})
        CryptoCompare._check_request_response_error({'Type': ERROR_TYPE_THRESHOLD + 1})

    def test_error_has_message(self):
        """Raised error should provide message if in response"""
        try:
            CryptoCompare._check_request_response_error({
                'Response': 'Error',
                'Message': 'Lorem ipsum dolor sit amet'
            })
        except CryptoCompareApiError as e:
            self.assertEqual(str(e), 'Lorem ipsum dolor sit amet')
        else:
            self.fail("Should have raised")


class TestGetCoinList(unittest.TestCase):
    def test_request(self):
        """Coin list should be returned on request"""
        cc = CryptoCompare()
        result = cc.get_coin_list()
        self.assertIn('BTC', result)
        self.assertIn('LTC', result)
        self.assertIn('ETH', result)


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


class TestGetCoinSnapshot(unittest.TestCase):
    def test_bitcoin_usd(self):
        """Requesting coin snapshot for BTC/USD should work"""
        cc = CryptoCompare()
        result = cc.get_coin_snapshot('BTC', 'USD')
        self.assertGreater(len(result), 0)

    def test_unknown_pair(self):
        """Requesting coin snapshot for an unknown pair should fail"""
        cc = CryptoCompare()
        self.assertRaises(CryptoCompareApiError, cc.get_coin_snapshot, 'XCSGS', 'DFGHGFD')


class TestGetCoinSnapshotFullById(unittest.TestCase):
    def test_bitcoin(self):
        """Requesting full coin snapshot for BTC should work"""
        cc = CryptoCompare()
        result = cc.get_coin_snapshot_full_by_id(BTC_ID)  # BTC id
        self.assertEqual(result['General']['Symbol'], 'BTC')

    def test_unknown_id(self):
        """Requesting full coin snapshot for unknown id should fail"""
        cc = CryptoCompare()
        self.assertRaises(
            CryptoCompareApiError,
            cc.get_coin_snapshot_full_by_id,
            9E9
        )


class TestGetSocialStats(unittest.TestCase):
    def test_bitcoin(self):
        """Requesting social stats for BTC should work"""
        cc = CryptoCompare()
        result = cc.get_social_stats(BTC_ID)  # BTC id
        self.assertEqual(result['General']['Name'], 'BTC')


class TestGetMiningContracts(unittest.TestCase):
    def test_request(self):
        """Mining contracts should be returned on request"""
        cc = CryptoCompare()
        result = cc.get_mining_contracts()
        self.assertGreater(len(result), 0)


class TestGetMiningEquipement(unittest.TestCase):
    def test_request(self):
        """Mining equipement should be returned on request"""
        cc = CryptoCompare()
        result = cc.get_mining_equipement()
        self.assertGreater(len(result), 0)


class TestGetTopPairs(unittest.TestCase):
    def test_bitcoin(self):
        """Request BTC top pairs should work"""
        cc = CryptoCompare()
        result = cc.get_top_pairs('BTC')
        self.assertGreater(len(result), 0)

    def test_bitcoin_lowercase(self):
        """Request lowercase written BTC top pairs should work"""
        cc = CryptoCompare()
        result = cc.get_top_pairs('btc')
        self.assertGreater(len(result), 0)

    def test_unknown_symbol(self):
        """Requesting unknown symbol top pairs should fail"""
        cc = CryptoCompare()
        self.assertRaises(CryptoCompareApiError, cc.get_top_pairs, 'XZSDFE')

    def test_specific_limit(self):
        """Request top pairs with a specific limit should return that many pairs (at most)"""
        cc = CryptoCompare()
        result = cc.get_top_pairs('BTC', limit=10)
        self.assertEqual(len(result), 10)

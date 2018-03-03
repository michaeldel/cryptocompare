============================
CryptoCompare API wrapper
============================
.. image:: https://travis-ci.org/michaeldel/cryptocompare.svg?branch=master
    :target: https://travis-ci.org/michaeldel/cryptocompare

Python API wrapper for CryptoCompare making retrieving data from that service simple and clean.

Example usage
=============

.. code-block:: python

    from cryptocompare import CryptoCompare

    cc = CryptoCompare()
    price = cc.get_price('BTC', 'USD')['BTC']['USD']

    print("1 BTC is worth {} USD".format(price))
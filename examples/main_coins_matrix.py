from cryptocompare import CryptoCompare

COINS = ['BTC', 'LTC', 'ETH', 'BCH', 'USD', 'EUR']

cc = CryptoCompare()
prices = cc.get_price(COINS, COINS)

print(end='\t')
for coin in COINS:  # top header
    print(coin, end='\t')

for a in COINS:
    print('\n', a, end='\t')  # left header
    for b in COINS:
        print('{:7.2f}'.format(prices[a][b]), end='\t')

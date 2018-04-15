import datetime
import matplotlib.pyplot as plt

from cryptocompare import CryptoCompare, CryptoCompareApiError, Period

BASE = 'ETH'
QUOTE = 'USD'

cc = CryptoCompare()

# prices need to be read in a loop because of cryptocompare's historical prices
# points limit
points = []
ts = None
while True:
    try:
        data = cc.get_historical(BASE, QUOTE, period=Period.MINUTE, limit=100000, to_ts=ts)
    except CryptoCompareApiError:
        break

    # first price is the oldest one, remove one to not include that point again
    ts = data[0]['time']
    print("Got historical data from {} ({} points)".format(ts, len(data)))

    data.extend(points)
    points = data

closes = [p['close'] for p in points]
datetimes = [datetime.datetime.fromtimestamp(p['time']) for p in points]

plt.plot(datetimes, closes)
plt.show()

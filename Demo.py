from yahooquery import Ticker

# It's incredibly easy to instantiate.  Just pass a symbol or list of symbols

# Instantiate with 'aapl' (Apple, Inc.)
aapl = Ticker('aapl')

# Multiple symbols can be passed as well
tickers = Ticker(['aapl', 'fb', 'msft', 'goog'])

# You can also pass multiple symbols as a string
tickers = Ticker('btc-usd fb msft goog')
print(tickers.summary_detail)
from yahooquery import Ticker
import requests

def GetSingleStock(tickerString):
    tickers = Ticker(tickerString)
    return tickers
def GetAllStocks(tickerString):
    tickers = Ticker(tickerString)
    return tickers


def get_symbol_list(symbol):
    url = "https://query1.finance.yahoo.com/v1/finance/search?q={}".format(symbol)

    result = requests.get(url).json()

    for x in result['ResultSet']['Result']:
        if x['symbol'] == symbol:
            return x['name']



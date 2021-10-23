from yahooquery import Ticker
def GetSingleStock(tickerString):
    tickers = Ticker(tickerString)
    return tickers
def GetAllStocks(tickerString):
    tickers = Ticker(tickerString)
    return tickers
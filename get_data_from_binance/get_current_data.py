from datetime import datetime
import time

from binance.client import Client
from .keys import api_key, api_secret

client = Client(api_key, api_secret)

today = datetime.now()
datem = datetime(today.year, today.month, 1)
price_name_jun = "price2020-06-01"
price_name_now = f"price{datem.strftime('%Y')}-{datem.strftime('%m')}-{datem.strftime('%d')}"

def get_current_data(client_binance=client) -> list:
    # get today prices
    prices = client_binance.get_all_tickers()
    for e in prices:
        e[price_name_now] = e['price']
        del e['price']
    # filter only USDT pairs
    USDT_pairs = [e for e in prices if e['symbol'].endswith("USDT")]
    # now generate list of all USDT pairs of hight values
    print("starting")
    for e in USDT_pairs:
        try:
            val_ = client_binance.get_historical_klines(e['symbol'], Client.KLINE_INTERVAL_1WEEK, "1 Jun, 2020")[0]
            # print(e, len(val_), end=" ")
            val_ = val_[2]
            # print(val_)
        except IndexError:
            val_ = None
        e[price_name_jun] = val_
    print("done")
    return USDT_pairs

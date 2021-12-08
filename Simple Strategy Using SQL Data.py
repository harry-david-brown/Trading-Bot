from binance import Client, BinanceSocketManager, AsyncClient
import asyncio
import sqlite3
import pandas as pd
import sqlalchemy
import matplotlib.pyplot as plt


api_key = "zoMhVAOpfwC2qRkLTpXJDWvMfhFRnXK9OEc4cv99mGgpkMHyLvEgYqyIrZ4XmTmd"
api_secret = "CmcbnCYecEWyvFWL83rToKSZHsEGzXIPPIo5beXz98ZPWMhD4LSyioxvgSyqSG8h"
client = Client(api_key, api_secret)

engine = sqlalchemy.create_engine('sqlite:///OurDatabase.db')


def strategy(entry, lookback, qty, open_position=False):
    while True:
        df = pd.read_sql('BTCUSDT', engine)
        lookbackperiod = df.iloc[-lookback:]
        cumret = (lookbackperiod.Price.pct_change() + 1).cumprod() - 1

        if not open_position:
            if cumret[cumret.last_valid_index()] > entry:
                #order = client.create_order(symbol='BTCUSDT',
                #side='BUY',
                #type='MARKET',
                #quantity=qty)

                #print(order)
                #open_position=True
                break

        if open_position:
            #sincebuy = df.loc[df.Time > pd.to_datetime(order['transactTime'],
            #                                        unit='ms')]
            #if len(sincebuy) > 1:
            #sincebuyret = (sincebuy.Price.pct_change() + 1).cumprod() - 1
            #last_entry = sincebuyret[sincebuyret.last_valid_index()]
            #if last_entry > 0.0015 or last_entry < -0.0015:
            #order = client.create_order(symbol='BTCUSDT',
            #side='SELL',
            #type='MARKET',
            #quantity=qty)
            #print(order)

            break


strategy(1, 60, 1)

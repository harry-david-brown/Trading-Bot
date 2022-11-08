from binance import Client, BinanceSocketManager, AsyncClient
import pandas as pd
import matplotlib.pyplot as plt
import sqlalchemy
import asyncio

api_key = "zoMhVAOpfwC2qRkLTpXJDWvMfhFRnXK9OEc4cv99mGgpkMHyLvEgYqyIrZ4XmTmd"
api_secret = "CmcbnCYecEWyvFWL83rToKSZHsEGzXIPPIo5beXz98ZPWMhD4LSyioxvgSyqSG8h"

client = Client(api_key, api_secret)
bsm = BinanceSocketManager(client)
socket = bsm.trade_socket('BTCUSDT')


async def main():
    await socket.__aenter__()
    msg = await socket.recv()
    test = createframe(msg)
    print(test)


def createframe(msg):
    df = pd.DataFrame([msg])
    df = df.loc[:, ['s', 'E', 'p']]
    df.columns = ['Symbol', 'Time', 'Price']
    df.Price = df.Price.astype(float)
    df.Time = pd.to_datetime(df.Time, unit='ms')
    return df


loop = asyncio.get_event_loop()
loop.run_until_complete(main())

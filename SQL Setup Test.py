from binance import Client, BinanceSocketManager, AsyncClient
import sqlite3
import pandas as pd
import sqlalchemy
import asyncio


api_key = "zoMhVAOpfwC2qRkLTpXJDWvMfhFRnXK9OEc4cv99mGgpkMHyLvEgYqyIrZ4XmTmd"
api_secret = "CmcbnCYecEWyvFWL83rToKSZHsEGzXIPPIo5beXz98ZPWMhD4LSyioxvgSyqSG8h"


client = Client(api_key, api_secret)
bsm = BinanceSocketManager(client)
socket = bsm.trade_socket('BTCUSDT')


async def main():

    try:
        connection = sqlite3.connect('OurDatabase.db')
        print("Connected to OurDatabase.db")
    except:
        print("Couldn't connect to database.")

    cursor = connection.cursor()
    cursor.execute('DELETE FROM BTCUSDT')
    connection.commit()
    print("Table clear")

    engine = sqlalchemy.create_engine('sqlite:///OurDatabase.db')

    while True:
        await socket.__aenter__()
        msg = await socket.recv()
        frame = createframe(msg)
        frame.to_sql('BTCUSDT', engine, if_exists='append', index=False)
        print(frame)


def createframe(msg):
    df = pd.DataFrame([msg])
    df = df.loc[:, ['s', 'E', 'p']]
    df.columns = ['Symbol', 'Time', 'Price']
    df.Price = df.Price.astype(float)
    df.Time = pd.to_datetime(df.Time, unit='ms')
    return df


loop = asyncio.get_event_loop()
loop.run_until_complete(main())

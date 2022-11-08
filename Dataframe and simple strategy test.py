from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
import pandas as pd
import matplotlib.pyplot as plt
import sqlalchemy

api_key = "zoMhVAOpfwC2qRkLTpXJDWvMfhFRnXK9OEc4cv99mGgpkMHyLvEgYqyIrZ4XmTmd"
api_secret = "CmcbnCYecEWyvFWL83rToKSZHsEGzXIPPIo5beXz98ZPWMhD4LSyioxvgSyqSG8h"

client = Client(api_key, api_secret)

"""
# client account
print(client.get_account())

# datastream via websocket
print(pd.DataFrame(client.get_historical_klines('BTCUSDT', '1m', '30 m ago UTC')))
# all strings, ex: ('BTCUSDT', '1m', '30 m ago UTC')
"""


def getminutedata(symbol, interval, time):
    frame = pd.DataFrame(client.get_historical_klines(
        symbol, interval, time+' m ago UTC'))

    frame = frame.iloc[:, :6]
    frame.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    frame = frame.set_index('Time')
    frame.index = pd.to_datetime(frame.index, unit='ms')
    frame = frame.astype(float)

    return frame


"""
test = getminutedata('BTCUSDT', '1m', '30')
print(test)
# Plot minutedata on graph
plt.plot(test.Open)
plt.show()
"""


def strategytest(symbol, qty, entried=False):
    df = getminutedata(symbol, '1m', '30')
    # cumulative return is just total return over a time window
    cumulret = (df.Open.pct_change() + 1).cumprod() - 1
    print(cumulret)
    if not entried:
        if cumulret[-1] < -0.002:
            order = client.create_order(
                symbol=symbol, side='BUY', type='MARKET', quantity=qty)
            print(order)
            entried = True
        else:
            print("No trade has been executed")

        if entried:
            while True:
                df = getminutedata(symbol, '1m', '30')
                sincebuy = df.loc[df.index > pd.to_datetime(
                    order['transactTime'], unit='ms')]
                if len(sincebuy) > 0:
                    sincebuyret = (
                        sincebuy.Open.pct_change() + 1).cumprod() - 1
                    if sincebuyret[-1] > 0.0015 or sincebuyret < -0.0015:
                        order = client.create_order(
                             symbol=symbol, side='SELL', type='MARKET',
                             quantity=qty)
                        print(order)
                        break


# strategytest('BNBUSDT', 0.0008)

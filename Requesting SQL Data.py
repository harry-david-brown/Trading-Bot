import sqlite3
import pandas as pd
import sqlalchemy
import matplotlib.pyplot as plt

engine = sqlalchemy.create_engine('sqlite:///OurDatabase.db')

df = pd.read_sql('BTCUSDT', engine)
df.Price.plot()
plt.show()

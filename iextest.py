from iexfinance import Stock
from iexfinance import get_historical_data
from datetime import datetime
tsla = Stock('TSLA')
print("open", tsla.get_open())
print("volume", tsla.get_volume())
print("price", tsla.get_price())
print("close", tsla.get_close())

start = datetime(2018,10,11)
end = datetime(2018,10,13)

df = get_historical_data("AAPL", start = start, end = end, output_format = 'pandas')
print(df.head())


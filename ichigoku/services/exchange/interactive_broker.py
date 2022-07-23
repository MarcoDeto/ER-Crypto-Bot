import pytz # pip install ibpy-native
from ibapi import contract as ib_contract
from ibpy_native import bridge as ibpy_bridge
from ib_insync import * # pip install ib_insync

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)

contract = Forex('EURJPY')
bars = ib.reqHistoricalData(
    contract, endDateTime='', durationStr='30 D',
    barSizeSetting='1 hour', whatToShow='ASK', useRTH=True
)
df = util.df(bars)
print(df)

market_data = ib.reqMktData(contract, '', False, False)
print(market_data)

ib.run()
from tradingview_ta import TA_Handler, Interval, Exchange
import tradingview_ta

print(tradingview_ta.__version__)
# Example output: 3.1.3

handler = TA_Handler(
    symbol="BTCUSDT",
    exchange="BINANCE",
    screener="crypto",
    interval="1h",
    timeout=None
)

analysis = handler.get_analysis()

test = analysis.indicators["RSI"]

print(test)
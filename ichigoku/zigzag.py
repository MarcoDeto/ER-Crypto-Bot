import time
import numpy as np
import requests
import yfinance as yf # for getting stock price data
from zigzag import *
import pandas as pd
from datetime import datetime, timedelta

# Getting the data from yahoo finance
stock_data = yf.download(tickers='AAPL', period='1y', interval='1d')

stock_data.index = pd.to_datetime(stock_data.index)

# Define a series to store the pivots / inflections
pivots = peak_valley_pivots(stock_data['Adj Close'].values, 0.1, -0.1)

pivots = peak_valley_pivots_candlestick(X.values, 0.2, -0.2)
ts_pivots = pd.Series(X, index=X.index)
ts_pivots = ts_pivots[pivots != 0]
X.plot()
ts_pivots.plot(style='g-o');

dev_threshold = input.float(title="Deviation (%)", defval=5.0, minval=0.00001, maxval=100.0)
depth = 10
line_color = input(title="Line Color", defval='#2962FF')
extend_to_last_bar = input(title="Extend to Last Bar", defval=True)
display_reversal_price = input(title="Display Reversal Price", defval=True)
display_cumulative_volume = input(title="Display Cumulative Volume", defval=True)
display_reversal_price_change = input(title="Display Reversal Price Change", defval=True, inline="price rev")
difference_price = input.string("Absolute", "", options=["Absolute", "Percent"], inline="price rev")

def pivots(src, length, isHigh):
    p = nz(src[length])
    if length == 0
        [time, p]
    else
        isFound = true
        for i = 0 to math.abs(length - 1)
            if isHigh and src[i] > p
                isFound := false
            if not isHigh and src[i] < p
                isFound := false
        for i = length + 1 to 2 * length
            if isHigh and src[i] >= p
                isFound := false
            if not isHigh and src[i] <= p
                isFound := false
        if isFound and length * 2 <= bar_index
            [time[length], p]
        else
            [int(na), float(na)]

[iH, pH] = (highs, 5, True)
[iL, pL] = (lows, 5, False)

def calc_dev(base_price, price):
    100 * (price - base_price) / base_price

def price_rotation_aggregate(price_rotation, pLast, cum_volume):
    str = ""
    if display_reversal_price
        str += str.tostring(pLast, format.mintick) + " "
    if display_reversal_price_change
        str += price_rotation + " "
    if display_cumulative_volume
        str += "\n" + cum_volume
    str
    
def caption(isHigh, iLast, pLast, price_rotation, cum_volume):
    price_rotation_str = price_rotation_aggregate(price_rotation, pLast, cum_volume)
    if display_reversal_price or display_reversal_price_change or display_cumulative_volume
        if not isHigh
            label.new(iLast, pLast, text=price_rotation_str, style=label.style_none, xloc=xloc.bar_time, yloc=yloc.belowbar, textcolor=color.red)
        else
            label.new(iLast, pLast, text=price_rotation_str, style=label.style_none, xloc=xloc.bar_time, yloc=yloc.abovebar, textcolor=color.green)

def price_rotation_diff(pLast, price):
    if display_reversal_price_change:
        tmp_calc = price - pLast
        str = difference_price == "Absolute"? (math.sign(tmp_calc) > 0? "+" : "") + str.tostring(tmp_calc, format.mintick) : (math.sign(tmp_calc) > 0? "+" : "-") + str.tostring((math.abs(tmp_calc) * 100)/pLast, format.percent)
        str := "(" + str  + ")"
        str


lineLast = na
labelLast = na
iLast = 0
pLast = 0
isHighLast = True # otherwise the last pivot is a low pivot
linesCount = 0
sumVol = 0
sumVolLast = 0

def pivotFound(dev, isHigh, index, price):
	if isHighLast == isHigh and not na(lineLast):
        // same direction
        if isHighLast ? price > pLast : price < pLast
            if linesCount <= 1
                line.set_xy1(lineLast, index, price)
            line.set_xy2(lineLast, index, price)
            label.set_xy(labelLast, index, price)
            label.set_text(labelLast, price_rotation_aggregate(price_rotation_diff(line.get_y1(lineLast), price), price, str.tostring(sumVol + sumVolLast, format.volume)))
            [lineLast, labelLast, isHighLast, False, sumVol + sumVolLast]
        else:
            [line(na), label(na), bool(na), False, float(na)]
    else # reverse the direction (or create the very first line)
        if na(lineLast)
            id = line.new(index, price, index, price, xloc=xloc.bar_time, color=line_color, width=2)
            lb = caption(isHigh, index, price, price_rotation_diff(pLast, price),  str.tostring(sumVol, format.volume))
            [id, lb, isHigh, True, sumVol]
        else
            // price move is significant
            if math.abs(dev) >= dev_threshold
                id = line.new(iLast, pLast, index, price, xloc=xloc.bar_time, color=line_color, width=2)
                lb = caption(isHigh, index, price, price_rotation_diff(pLast, price),  str.tostring(sumVol, format.volume))
                [id, lb, isHigh, True, sumVol]
            else
                [line(na), label(na), bool(na), False, float(na)]

sumVol += nz(volume[math.floor(depth / 2)])

if not na(iH) and not na(iL) and iH == iL
    dev1 = calc_dev(pLast, pH)
    [id2, lb2, isHigh2, isNew2, sum2] = pivotFound(dev1, True, iH, pH)
    if isNew2
        linesCount := linesCount + 1
    if not na(id2)
        lineLast := id2
        labelLast := lb2
        isHighLast := isHigh2
        iLast := iH
        pLast := pH
        sumVolLast := sum2
        sumVol := 0
    dev2 = calc_dev(pLast, pL)
    [id1, lb1, isHigh1, isNew1, sum1] = pivotFound(dev2, False, iL, pL)
    if isNew1
        linesCount := linesCount + 1
    if not na(id1)
        lineLast := id1
        labelLast := lb1
        isHighLast := isHigh1
        iLast := iL
        pLast := pL
        sumVolLast := sum1
        sumVol := 0
else
    if not na(iH)
        dev1 = calc_dev(pLast, pH)
        [id, lb, isHigh, isNew, sum] = pivotFound(dev1, True, iH, pH)
        if isNew
            linesCount := linesCount + 1
        if not na(id)
            lineLast := id
            labelLast := lb
            isHighLast := isHigh
            iLast := iH
            pLast := pH
            sumVolLast := sum
            sumVol := 0
    else
        if not na(iL)
            dev2 = calc_dev(pLast, pL)
            [id, lb, isHigh, isNew, sum] = pivotFound(dev2, False, iL, pL)
            if isNew
                linesCount := linesCount + 1
            if not na(id)
                lineLast := id
                labelLast := lb
                isHighLast := isHigh
                iLast := iL
                pLast := pL
                sumVolLast := sum
                sumVol := 0

var line extend_line = na
var label extend_label = na
if extend_to_last_bar == True and barstate.islast == True
    isHighLastPoint = not isHighLast
    curSeries = isHighLastPoint ? high : low
    if na(extend_line) and na(extend_label)
        extend_line := line.new(line.get_x2(lineLast), line.get_y2(lineLast), time, curSeries, xloc=xloc.bar_time, color=line_color, width=2)
        extend_label := caption(not isHighLast, time, curSeries,  price_rotation_diff(line.get_y2(lineLast), curSeries), str.tostring(sumVol, format.volume))  
    line.set_xy1(extend_line, line.get_x2(lineLast), line.get_y2(lineLast))
    line.set_xy2(extend_line, time, curSeries)
    
    price_rotation = price_rotation_diff(line.get_y1(extend_line), curSeries)                                                                                                  
    remaingRealTimeVol = 0.
    for i = math.abs(math.floor(depth / 2) - 1) to 0
        remaingRealTimeVol += volume[i]
    label.set_xy(extend_label, time, curSeries)    
    label.set_text(extend_label, price_rotation_aggregate(price_rotation, curSeries, str.tostring(sumVol+remaingRealTimeVol, format.volume)))
    label.set_textcolor(extend_label, isHighLastPoint? color.green : color.red)
    label.set_yloc(extend_label, yloc= isHighLastPoint? yloc.abovebar : yloc.belowbar)
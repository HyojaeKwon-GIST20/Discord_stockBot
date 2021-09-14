from re import T
import time
from numpy import integer
import pyupbit
import datetime
from pyupbit.exchange_api import Upbit
import requests

ACCESS_CODE = ""
SECRET_CODE = ""

myToken = ""
upbit = pyupbit.Upbit(ACCESS_CODE,SECRET_CODE)


#현재 가격 조회
def getCurrentPrice(what):
  return pyupbit.get_orderbook(tickers=what)[0]["orderbook_units"][0]["ask_price"]

#시작 시간 조회
def startTime(what):
  df = pyupbit.get_ohlcv(what, interval="day", count=1)
  start_time = df.index[0]
  return start_time

#잔고 조회
def getBalance(what):
  balances = upbit.get_balances()
  for i in balances:
    if i['currency'] == what:
      if i['balance'] is not None:
        return float(i['balance'])
      else:
        return 0
  return 0

#15일 이평선 조회
def get15(what):
  df = pyupbit.get_ohlcv(what,interval='day',count=15)
  c15 = df['close'].rolling(15).mean().iloc[-1]
  return c15

#매수 목표가격 측정
def targetToBuy(what , alpha):
  df = pyupbit.get_ohlcv(what, interval="day", count=2)
  target = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * alpha
  return target


while True:
    try:
        now = datetime.datetime.now()
        start_time = startTime("KRW-BTC")
        end_time = start_time + datetime.timedelta(days=1)

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = targetToBuy("KRW-BTC", 0.5)
            ma15 = get15("KRW-BTC")
            current_price = getCurrentPrice("KRW-BTC")
            if target_price < current_price and ma15 < current_price:
                krw = getBalance("KRW")
                if krw > 5000:
                    buy_result = upbit.buy_market_order("KRW-BTC", krw*0.9995)
        else:
            btc = getBalance("BTC")
            if btc > 0.00008:
                sell_result = upbit.sell_market_order("KRW-BTC", btc*0.9995)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
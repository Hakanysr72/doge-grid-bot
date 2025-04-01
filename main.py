import time
import os
from binance.client import Client
from binance.enums import *

# Binance API bilgileri (Railway'de environment olarak tanımlanır)
API_KEY = os.environ.get("BINANCE_API_KEY")
API_SECRET = os.environ.get("BINANCE_API_SECRET")

client = Client(API_KEY, API_SECRET)

symbol = 'DOGEUSDT'
lower_price = 0.12
upper_price = 0.18
grid_count = 25
usdt_per_order = 25
quantity_precision = 0
price_precision = 5

price_step = (upper_price - lower_price) / grid_count
grid_levels = [round(lower_price + i * price_step, price_precision) for i in range(grid_count + 1)]

active_orders = {}

def get_current_price():
    try:
        ticker = client.get_symbol_ticker(symbol=symbol)
        return float(ticker['price'])
    except Exception as e:
        print(f"Fiyat alınamadı: {e}")
        return None

def place_limit_order(price, side):
    quantity = round(usdt_per_order / price)
    try:
        order = client.create_order(
            symbol=symbol,
            side=SIDE_BUY if side == 'BUY' else SIDE_SELL,
            type=ORDER_TYPE_LIMIT,
            timeInForce=TIME_IN_FORCE_GTC,
            quantity=quantity,
            price=format(price, f'.{price_precision}f')
        )
        print(f"{side} emri yerleştirildi: {price} USDT - {quantity} DOGE")
        return order
    except Exception as e:
        print(f"Emir hatası: {e}")
        return None

def grid_bot_loop():
    print("DOGE/USDT Grid bot çalışıyor (Railway sürümü)...")
    while True:
        try:
            price = get_current_price()
            if price is None:
                time.sleep(10)
                continue

            for i in range(1, len(grid_levels)):
                lower = grid_levels[i - 1]
                upper = grid_levels[i]

                if lower <= price < upper:
                    if i not in active_orders:
                        buy_order = place_limit_order(lower, 'BUY')
                        if buy_order:
                            active_orders[i] = {
                                'buy_price': lower,
                                'sell_price': upper
                            }

                    elif i in active_orders and price >= active_orders[i]['sell_price']:
                        place_limit_order(active_orders[i]['sell_price'], 'SELL')
                        print(f"Satış sonrası tekrar {active_orders[i]['buy_price']} seviyesine ALIM emri konuluyor...")
                        place_limit_order(active_orders[i]['buy_price'], 'BUY')

            time.sleep(10)

        except Exception as e:
            print(f"Bot hatası: {e}")
            time.sleep(15)

if __name__ == "__main__":
    grid_bot_loop()

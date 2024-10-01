import numpy as np
from botTelegram import send_message_to_telegram
from info import api, SYMBOL
import time, datetime as dt

def choose_order(choose, last_price):
    print("choose" + choose)
    if choose == 'buy':
        take_profit_price = last_price * 1.01
        stop_loss_price = last_price * 0.99
    elif choose == 'sell':
        take_profit_price = last_price * 0.99 
        stop_loss_price = last_price * 1.01

    api.submit_order(
        symbol=SYMBOL,
        qty=1,
        side=choose,
        type='market',
        time_in_force='gtc',
        order_class='bracket',  # Specifica che si tratta di un ordine complesso
        take_profit=dict(
            limit_price=take_profit_price  # Prezzo di take profit
        ),
        stop_loss=dict(
            stop_price=stop_loss_price      # Prezzo di stop loss
        )
    )
    message = f"{choose.capitalize()} ordine eseguito per {SYMBOL}!\n" \
              f"Prezzo di Take Profit: {take_profit_price}\n" \
              f"Prezzo di Stop Loss: {stop_loss_price}"
    send_message_to_telegram(message)
    
    time.sleep(60)
    print('Waiting...')


def read_market(close_list):
    start_date = (dt.datetime.now() - dt.timedelta(days=1)).replace(microsecond=0)  # Rimuove i microsecondi
    end_date = dt.datetime.now().replace(microsecond=0)  

    start_date_str = start_date.isoformat()
    end_date_str = end_date.isoformat()

    market_data = api.get_bars(symbol= SYMBOL, start=start_date_str, end=end_date_str, timeframe = '1Min', limit= 5)
    if(market_data is not None and len(market_data) > 1):
        close_list.clear()
        for bar in market_data:
            close_list.append(bar.c)
    else:
        print("No market data available")

    ma = np.mean(close_list)
    last_price = close_list[-1]

    print(f"Moving Average: {ma + 0.01}, Last Price: {last_price}")

    return ma, last_price

# def retrive_assets():
#     asset = api.get_asset(SYMBOL)
#     if(asset):
#         print(asset)

# def retrive_orders():
#     history = api.get_portfolio_history_for_account('0b6e6875-0151-4c72-9f8e-b78fef9b9eeb')
#     print (history)
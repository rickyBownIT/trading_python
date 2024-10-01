import time, datetime
from scripts import choose_order, read_market
from botTelegram import send_message_to_telegram

pos_held = False
close_list = []

while True:
    ma, last_price = read_market(close_list)

    print(f"condition = {ma + 0.01 < last_price and not pos_held}")
    if ma + 0.01 < last_price and not pos_held:
        choose_order('buy', last_price)
        pos_held = True

    elif ma - 0.01 > last_price and pos_held:
        choose_order('sell', last_price)
        pos_held = False
    else:
        send_message_to_telegram(f'No order at: {datetime.datetime.now()} \nMoving Avarage + 0.1: {ma + 0.1} \nLast Price: {last_price}')

    time.sleep(60)
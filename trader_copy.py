import random
import json

import argparse

if __name__ == '__main__':
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("RATE", type=str, nargs='?')
    args_parser.add_argument("AVAILABLE", type=str, nargs='?')
    args_parser.add_argument("BUY", type=int, nargs='?', default=0)
    args_parser.add_argument("SELL", type=int, nargs='?', default=0)
    args_parser.add_argument("BUY ALL", type=str, nargs='?')
    args_parser.add_argument("SELL ALL", type=str, nargs='?')
    args_parser.add_argument("NEXT", type=str, nargs='?')
    args_parser.add_argument("RESTART", type=str, nargs='?')

args = vars(args_parser.parse_args())
print(args)

with open('config.json', 'r') as f:
    config_data = json.load(f)
delta = config_data['delta']
initial_rate = config_data['initial_rate']

with open('status_system.json', 'r') as f:
    state = json.load(f)
UAH_BALANCE = state["uah_balance"]
USD_BALANCE = state["usd_balance"]
RATE = state["rate"]


def save_data():
    with open('status_system.json', 'w') as f:
        json.dump(state, f)


def change_rate(rate):
    new_rate = round(random.uniform(rate - delta, rate + delta), 2)
    state["rate"] = new_rate
    state["history"].append({"action": "NEXT", "rate": new_rate})
    save_data()
    return new_rate


def buy_usd(amount):
    global UAH_BALANCE, USD_BALANCE
    uah_amount = round(amount * RATE, 2)
    if UAH_BALANCE < uah_amount:
        state["history"].append({"action": "BUY USD - error", "amount": amount, "rate": RATE})
        save_data()
        print('UNAVAILABLE, REQUIRED BALANCE UAH {}, AVAILABLE {}'.format(uah_amount, UAH_BALANCE))
    else:
        state["uah_balance"] -= uah_amount
        state["usd_balance"] += amount
        state["history"].append({"action": "BUY USD", "amount": amount, "rate": RATE})
        save_data()
        print('SUCCESS, USD {} bought for UAH {}'.format(amount, uah_amount))


def sell_usd(amount):
    global UAH_BALANCE, USD_BALANCE
    uah_amount = round(amount * RATE, 2)
    if USD_BALANCE < amount:
        state["history"].append({"action": "SELL USD - error", "amount": amount, "rate": RATE})
        save_data()
        print('UNAVAILABLE, REQUIRED BALANCE USD {}, AVAILABLE {}'.format(USD_BALANCE, amount))
    else:
        state["usd_balance"] -= amount
        state["uah_balance"] += uah_amount
        state["history"].append({"action": "SELL USD", "amount": amount, "rate": RATE})
        save_data()
        print('SUCCESS, USD {} sold for UAH {}'.format(amount, uah_amount))


def buy_all():
    global UAH_BALANCE, USD_BALANCE
    usd_amount = int(UAH_BALANCE / RATE)
    uah_amount = round(usd_amount * RATE, 2)
    if UAH_BALANCE < uah_amount:
        state["history"].append({"action": "BUY USD ALL - error", "amount": USD_BALANCE, "rate": RATE})
        save_data()
        print('UNAVAILABLE, REQUIRED BALANCE UAH {}, AVAILABLE {}'.format(uah_amount, UAH_BALANCE))
    else:
        state["usd_balance"] += usd_amount
        state["uah_balance"] -= uah_amount
        state["history"].append({"action": "BUY USD ALL", "amount": USD_BALANCE, "rate": RATE})
        save_data()
        print('SUCCESS, USD {} bought for UAH {}'.format(usd_amount, uah_amount))


def handle_arguments(arg):
    if arg["RATE"]:
        print('Поточний курс: ', state["rate"])
        pass
    elif arg['NEXT']:
        random_rate = change_rate(initial_rate)
        print('Новий курс: ', random_rate)
        pass
    elif arg["BUY"]:
        amount = float(args["BUY"])
        buy_usd(amount)
        pass
    elif arg["SELL"]:
        amount = float(args["SELL"])
        sell_usd(amount)
        pass
    elif arg["BUY ALL"]:
        buy_all()
        pass


if any(args.values()):
    handle_arguments(args)
else:
    print("Error: pass valid argument.")



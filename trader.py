import random
import json
import sys

args = sys.argv[1:]

with open('config.json', 'r') as f:
    config_data = json.load(f)
delta = config_data['delta']
initial_rate = config_data['initial_rate']
initial_uah_balance = config_data['initial_uah_balance']
initial_usd_balance = config_data['initial_usd_balance']

with open('status_system.json', 'r') as f:
    state = json.load(f)
UAH_BALANCE = state["uah_balance"]
USD_BALANCE = state["usd_balance"]
RATE = state["rate"]


def save_data():
    with open('status_system.json', 'w') as f:
        json.dump(state, f)


def get_history():
    print(f"Operations history: {state['history']}")

def restart():
    state["usd_balance"] = initial_usd_balance
    state["uah_balance"] = initial_uah_balance
    state["rate"] = initial_rate
    state["history"] = []
    save_data()
    print(f"Data was reset: {state['uah_balance']} UAH, {state['usd_balance']} USD, Rate - {state['rate']}")


def change_rate(rate):
    new_rate = round(random.uniform(rate - delta, rate + delta), 2)
    state["rate"] = new_rate
    state["history"].append({"action": "NEXT", "rate": new_rate})
    save_data()
    return new_rate


def buy_usd(amount):
    uah_amount = round(amount * RATE, 2)
    if UAH_BALANCE < uah_amount:
        state["history"].append({"action": "BUY USD - error", "amount": amount, "rate": RATE})
        print('UNAVAILABLE, REQUIRED BALANCE UAH {}, AVAILABLE {}'.format(uah_amount, UAH_BALANCE))
        save_data()
    else:
        state["uah_balance"] = round(UAH_BALANCE - uah_amount, 2)
        state["usd_balance"] = round(USD_BALANCE + amount, 2)
        state["history"].append({"action": "BUY USD", "amount": amount, "rate": RATE})
        print('SUCCESS, USD {} bought for UAH {}'.format(amount, uah_amount))
        save_data()


def sell_usd(amount):
    uah_amount = round(amount * RATE, 2)
    if USD_BALANCE < amount:
        state["history"].append({"action": "SELL USD - error", "amount": amount, "rate": RATE})
        print('UNAVAILABLE, REQUIRED BALANCE USD {}, AVAILABLE {}'.format(USD_BALANCE, amount))
        save_data()
    else:
        state["usd_balance"] = round(USD_BALANCE - amount, 2)
        state["uah_balance"] = round(UAH_BALANCE + uah_amount, 2)
        state["history"].append({"action": "SELL USD", "amount": amount, "rate": RATE})
        print('SUCCESS, USD {} sold for UAH {}'.format(amount, uah_amount))
        save_data()


def buy_all():
    usd_amount = round(UAH_BALANCE / RATE, 2)
    uah_amount = round(usd_amount * RATE, 2)

    if UAH_BALANCE < uah_amount or usd_amount < (0.01 * RATE):
        state["history"].append({"action": "BUY USD ALL - error", "amount": USD_BALANCE, "rate": RATE})
        print('UNAVAILABLE, BALANCE UAH {}, not enough money'.format(UAH_BALANCE))
        save_data()
    else:
        state["usd_balance"] = round(USD_BALANCE + usd_amount, 2)
        state["uah_balance"] = round(UAH_BALANCE - uah_amount, 2)
        state["history"].append({"action": "BUY USD ALL", "amount": USD_BALANCE, "rate": RATE})
        print('SUCCESS, USD {} buy for UAH {}'.format(usd_amount, uah_amount))
        save_data()


def sell_all():
    if USD_BALANCE == 0:
        state["history"].append({"action": "SELL USD ALL - error", "amount": 0, "rate": RATE})
        print('UNAVAILABLE, BALANCE USD {}'.format(USD_BALANCE))
        save_data()
    else:
        sell_amount = round(USD_BALANCE * state["rate"], 2)
        state["usd_balance"] = 0
        state["uah_balance"] = round(UAH_BALANCE + sell_amount, 2)
        state["history"].append({"action": "SELL USD ALL", "amount": USD_BALANCE, "rate": RATE})
        print('SUCCESS, USD {} sold for UAH {}'.format(USD_BALANCE, sell_amount))
        save_data()


def get_account_balance():
    state["history"].append({"action": "AVAILABLE", "uah_balance": UAH_BALANCE, "usd_balance": USD_BALANCE})
    save_data()
    print(f"Balance on your accounts: {state['uah_balance']} UAH and {state['usd_balance']} USD")


if len(args) > 0:
    if 'RATE' in args:
        state["history"].append({"action": "RATE", "rate": RATE})
        save_data()
        print('Current rate: ', state["rate"])
        pass
    elif 'NEXT' in args:
        random_rate = change_rate(initial_rate)
        print('New rate: ', random_rate)
        pass
    elif 'BUY' in args and args[1] != "ALL":
        amount = float(args[args.index('BUY') + 1])
        buy_usd(amount)
        pass
    elif "SELL" in args and args[1] != "ALL":
        amount = float(args[args.index('SELL') + 1])
        sell_usd(amount)
        pass
    elif args[0] == "BUY" and args[1] == "ALL":
        buy_all()
        pass
    elif args[0] == "SELL" and args[1] == "ALL":
        sell_all()
        pass
    elif "AVAILABLE" in args:
        get_account_balance()
        pass
    elif "RESTART" in args:
        restart()
        pass
    elif "HISTORY" in args:
        get_history()
        pass
    else:
        print("Error: pass valid argument.")

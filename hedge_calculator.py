# Hedging calculator
# A punter has backed a horse with a bookmaker. How much should the bookmaker
# back it for on the exchange, so they make the same profit win or lose?


def ask_number(question, default=None, allow_zero=False):
    """Keep asking until a valid number is typed."""
    while True:
        answer = input(question).strip()
        if answer == "" and default is not None:
            return default
        try:
            number = float(answer)
        except ValueError:
            print("  Please type a number, like 100 or 3.5")
            continue
        if number < 0 or (number == 0 and not allow_zero):
            print("  Please type a number bigger than 0")
            continue
        return number


punter_stake = ask_number("Punter's stake (£): ")
bookie_price = ask_number("Price the punter got (decimal, e.g. 3.0): ")
exchange_price = ask_number("Exchange back price (decimal, e.g. 5.0): ")
commission = ask_number("Exchange commission % (press Enter for 5): ", default=5.0, allow_zero=True) / 100

if bookie_price <= 1 or exchange_price <= 1:
    print("Decimal prices must be bigger than 1.0.")
    raise SystemExit

# Pick the exchange stake that makes both outcomes equal:
#   horse wins:  -punter_stake * (bookie_price - 1) + back_stake * (exchange_price - 1) * (1 - commission)
#   horse loses: +punter_stake - back_stake
back_stake = punter_stake * bookie_price / (1 + (exchange_price - 1) * (1 - commission))

if_wins = -punter_stake * (bookie_price - 1) + back_stake * (exchange_price - 1) * (1 - commission)
if_loses = punter_stake - back_stake

print()
print(f"Back £{back_stake:.2f} on the exchange at {exchange_price}")
print(f"  If the horse wins:  £{if_wins:+.2f}")
print(f"  If the horse loses: £{if_loses:+.2f}")
print()

if if_loses > 0:
    print("Profit locked in, whatever happens.")
else:
    print("Warning: the exchange price isn't big enough to lock in a profit.")
    print("Hedging here only limits the loss.")

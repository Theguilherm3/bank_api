def transaction_tax(type, amount):
    if type == "D":
        amount *= 1.03
    elif type == "C":
        amount *= 1.05
    return amount

from pathlib import Path
from enum import Enum
from abc import ABC, abstractmethod


class Everything(ABC):
    @abstractmethod
    def send(self, x):
        pass

    @abstractmethod
    def save(self, x):
        pass

    @abstractmethod
    def refund(self, x):
        pass


class Order(Everything):
    # def __init__(self, orderStringRepresentation):

    def send(self, x):
        print("EMAIL " + x)

    def save(self, x):
        with Path("orders.txt").open("a", encoding="utf-8") as f:
            f.write(x + "\n")

    def refund(self, x):
        raise NotImplementedError("Not supported")

counter = 0
total = 0

def getProductPrice(product):
    if product == "BOOK":
        return 40
    elif product == "PEN":
        return 5
    elif product == "BAG":
        return 80
    else:
        return 0

class Action(Enum):
    ORDER = 1
    REPORT = 2

class MemberType(Enum):
    REGULAR = 1
    VIP = 2
    STUDENT = 3

DISCOUNTS = {
    "SAVE10": 0.9,
    MemberType.REGULAR: 1.0,
    MemberType.VIP: 0.9,
    MemberType.STUDENT: 0.95
}

def applyDiscount(price, discountReason):
    return price * DISCOUNTS.get(discountReason, 1.0)

FREE_DELIVERY_THRESHOLD = 100
DELIVERY_COST = 12

def applyDeliveryCost(price):
    if price < FREE_DELIVERY_THRESHOLD:
        price += DELIVERY_COST
    return price

TAXES_PERCENTAGE = 0.23

def applyTaxes(price):
    return price * (1 + TAXES_PERCENTAGE)



def order(orderInformationString, action, verbose, send, save):
    global counter, total
    orderInformation = orderInformationString.split("|")
    n, e, t = orderInformation[0], orderInformation[1], orderInformation[2]
    products = orderInformation[3].split(",")
    price = 0
    detail = ""
    for q in products:
        c = q.split(":")
        
        p = getProductPrice(c[0])
        price += p * int(c[1])
        detail += c[0] + "x" + c[1] + ";"

    price = applyDiscount(price, MemberType[t])
    price = applyDiscount(price, orderInformation[4])

    price = applyDeliveryCost(price)
    price = applyTaxes(price)

    orderDescription = f"ORDER|{n}|{detail}|{price:.2f}"
    counter += 1
    total += price
    obj = Order()

    try:
        if save:
            obj.save(orderDescription)
        if send:
            obj.send(e + "|" + orderDescription)
        if verbose:
            print(orderDescription)
        return orderDescription
    except Exception:
        return "ERROR"


def showReport():
    global counter, total
    orderDescription = f"REPORT|{counter}|{total:.2f}"
    print(orderDescription)


def executeAction(command, info = "", verbose = True, send = True, save = True):
    match command:
        case Action.ORDER:
            return order(info, Action.ORDER, verbose, send, save)
        case Action.REPORT:
            return showReport()
        case _:
            return "UNKNOWN"



if __name__ == "__main__":
    executeAction(Action.ORDER, "Alice|alice@example.test|VIP|BOOK:2,PEN:3|SAVE10", True, True, True)
    executeAction(Action.ORDER, "Bob|bob@example.test|REGULAR|BAG:2|NONE", True, True, True)
    executeAction(Action.REPORT)

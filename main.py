from pathlib import Path
from enum import Enum
# from abc import ABC, abstractmethod


# class Everything(ABC):
#     @abstractmethod
#     def send(self, x):
#         pass

#     @abstractmethod
#     def save(self, x):
#         pass

#     @abstractmethod
#     def refund(self, x):
#         pass


class Order:
    def send(self, x):
        print("EMAIL " + x)

    def save(self, x):
        with Path("orders.txt").open("a", encoding="utf-8") as f:
            f.write(x + "\n")

    def refund(self, x):
        raise NotImplementedError("Not supported")


PRODUCT_PRICE = {
    "BOOK": 40,
    "PEN": 5,
    "BAG": 80,
}


counter = 0
total = 0


def order(orderInformationString, verbose, send, save):
    global counter, total
    try:
        orderInformation = orderInformationString.split("|")
        n, e, t = orderInformation[0], orderInformation[1], orderInformation[2]
        products = orderInformation[3].split(",")
        price = 0
        detail = ""
        for q in products:
            c = q.split(":")
            price += PRODUCT_PRICE.get(c[0], 0) * int(c[1])
            detail += c[0] + "x" + c[1] + ";"
        price *= DISCOUNTS.get(MemberType[t], 1.0)
        price *= DISCOUNTS.get(orderInformation[4], 1.0)
        if price < FREE_DELIVERY_THRESHOLD:
            price += DELIVERY_COST
        price *= 1 + TAXES_PERCENTAGE
        orderDescription = f"ORDER|{n}|{detail}|{price:.2f}"
        counter += 1
        total += price
        obj = Order()
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
    print(f"REPORT|{counter}|{total:.2f}")


def executeAction(command, info="", verbose=True, send=True, save=True):
    if command == Action.ORDER:
        return order(info, verbose, send, save)
    if command == Action.REPORT:
        return showReport()
    return "UNKNOWN"


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
    MemberType.STUDENT: 0.95,
}


FREE_DELIVERY_THRESHOLD = 100
DELIVERY_COST = 12


TAXES_PERCENTAGE = 0.23


if __name__ == "__main__":
    executeAction(
        Action.ORDER,
        "Alice|alice@example.test|VIP|BOOK:2,PEN:3|SAVE10",
        True,
        True,
        True,
    )
    executeAction(
        Action.ORDER, "Bob|bob@example.test|REGULAR|BAG:2|NONE", True, True, True
    )
    executeAction(Action.REPORT)

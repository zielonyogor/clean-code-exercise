from pathlib import Path
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
            if c[0] == "BOOK":
                p = 40
            elif c[0] == "PEN":
                p = 5
            elif c[0] == "BAG":
                p = 80
            else:
                p = 0
            price += p * int(c[1])
            detail += c[0] + "x" + c[1] + ";"
        if t == "VIP":
            price *= 0.9
        elif t == "STUDENT":
            price *= 0.95
        if orderInformation[4] == "SAVE10":
            price *= 0.9
        if price < 100:
            price += 12
        price *= 1.23
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
    if command == 1:
        return order(info, verbose, send, save)
    if command == 2:
        return showReport()
    return "UNKNOWN"


if __name__ == "__main__":
    executeAction(1, "Alice|alice@example.test|VIP|BOOK:2,PEN:3|SAVE10", True, True, True)
    executeAction(1, "Bob|bob@example.test|REGULAR|BAG:2|NONE", True, True, True)
    executeAction(2)

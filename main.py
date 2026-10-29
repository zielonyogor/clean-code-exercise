from pathlib import Path
from enum import Enum
from decimal import Decimal
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
    def __init__(self, orderStringRepresentation):
        self.details = self.OrderDetails(orderStringRepresentation)

    class ProductsHolder:
        def __init__(self, productsStringRepresentation):
            self.products = []
            for productWithQuantity in productsStringRepresentation.split(','):
                product, quantityStr = productWithQuantity.split(":")
                self.products.append([product, int(quantityStr)])

        def getTotalPrice(self):
            return sum([getProductPrice(product) * quantity for product, quantity in self.products])

        def __str__(self):
            return "".join(f"{product}x{quantity};" for product, quantity in self.products)

    class OrderDetails:
        def __init__(self, orderStringRepresentation):
            self.__extractDetails(orderStringRepresentation)

        def __extractDetails(self, orderStringRepresentation):
            orderInformation = orderStringRepresentation.split("|")
            self.name = orderInformation[0]
            self.email = orderInformation[1]
            self.memberType = MemberType[orderInformation[2]]
            self.products = Order.ProductsHolder(orderInformation[3])
            self.discountCode = orderInformation[4]

    def send(self, x):
        print("EMAIL " + x)

    def save(self, x):
        with Path("orders.txt").open("a", encoding="utf-8") as f:
            f.write(x + "\n")

    def refund(self, x):
        raise NotImplementedError("Not supported")


def getProductPrice(product):
    PRODUCT_PRICE = {
        "BOOK": Decimal(40),
        "PEN": Decimal(5),
        "BAG": Decimal(80),
    }

    return PRODUCT_PRICE.get(product, 0)


class OrderProcessor:
    def __init__(self):
        self.counter = 0
        self.total = 0

    def _order(self, orderInformationString, verbose, send, save):
        obj = Order(orderInformationString)
        details = obj.details

        price = details.products.getTotalPrice()
        detail = str(details.products)

        price = applyDiscount(price, details.memberType)
        price = applyDiscount(price, details.discountCode)

        price = applyDeliveryCost(price)
        price = applyTaxes(price)

        orderDescription = f"ORDER|{details.name}|{detail}|{price:.2f}"
        self.counter += 1
        self.total += price

        try:
            if save:
                obj.save(orderDescription)
            if send:
                obj.send(details.email + "|" + orderDescription)
            if verbose:
                print(orderDescription)
            return orderDescription
        except Exception:
            return "ERROR"

    def _showReport(self):
        print(f"REPORT|{self.counter}|{self.total:.2f}")

    def executeAction(self, command, info="", verbose=True, send=True, save=True):
        if command == Action.ORDER:
            return self._order(info, verbose, send, save)
        if command == Action.REPORT:
            return self._showReport()
        return "UNKNOWN"


class Action(Enum):
    ORDER = 1
    REPORT = 2


class MemberType(Enum):
    REGULAR = 1
    VIP = 2
    STUDENT = 3


DISCOUNTS = {
    "SAVE10": Decimal(0.9),
    MemberType.REGULAR: Decimal(1.0),
    MemberType.VIP: Decimal(0.9),
    MemberType.STUDENT: Decimal(0.95),
}


def applyDiscount(price, discountReason):
    return price * DISCOUNTS.get(discountReason, Decimal(1.0))


FREE_DELIVERY_THRESHOLD = Decimal(100)
DELIVERY_COST = Decimal(12)


def applyDeliveryCost(price):
    if price < FREE_DELIVERY_THRESHOLD:
        price += DELIVERY_COST
    return price


TAXES_PERCENTAGE = Decimal(0.23)


def applyTaxes(price):
    return price * (1 + TAXES_PERCENTAGE)


if __name__ == "__main__":
    processor = OrderProcessor()

    processor.executeAction(
        Action.ORDER,
        "Alice|alice@example.test|VIP|BOOK:2,PEN:3|SAVE10",
        True,
        True,
        True,
    )
    processor.executeAction(
        Action.ORDER, "Bob|bob@example.test|REGULAR|BAG:2|NONE", True, True, True
    )
    processor.executeAction(Action.REPORT)

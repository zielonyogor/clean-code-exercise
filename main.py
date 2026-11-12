from pathlib import Path
from enum import Enum
from decimal import Decimal


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

    def send(self, message):
        print("EMAIL " + message)

    def save(self, orderDescription):
        with Path("orders.txt").open("a", encoding="utf-8") as f:
            f.write(orderDescription + "\n")


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

    def order(self, orderInformationString, verbose=True, send=True, save=True):
        order = Order(orderInformationString)
        details = order.details

        price = calculatePrice(details)
        productsDescription = str(details.products)

        orderDescription = f"ORDER|{details.name}|{productsDescription}|{price:.2f}"
        self.counter += 1
        self.total += price

        try:
            if save:
                order.save(orderDescription)
            if send:
                order.send(details.email + "|" + orderDescription)
            if verbose:
                print(orderDescription)
            return orderDescription
        except Exception:
            return "ERROR"

    def report(self):
        print(f"REPORT|{self.counter}|{self.total:.2f}")


def calculatePrice(details):
    price = details.products.getTotalPrice()
    price = applyMemberDiscount(price, details.memberType)
    price = applyCouponDiscount(price, details.discountCode)
    price = applyDeliveryCost(price)
    return applyTaxes(price)


def handleCommand(processor, commandLine):
    command, _, payload = commandLine.partition(" ")
    if command == "ORDER":
        return processor.order(payload)
    if command == "REPORT":
        return processor.report()
    return "UNKNOWN"


class MemberType(Enum):
    REGULAR = 1
    VIP = 2
    STUDENT = 3


MEMBER_DISCOUNTS = {
    MemberType.REGULAR: Decimal("1.0"),
    MemberType.VIP: Decimal("0.9"),
    MemberType.STUDENT: Decimal("0.95"),
}

COUPON_DISCOUNTS = {
    "SAVE10": Decimal("0.9"),
}


def applyMemberDiscount(price, memberType):
    return price * MEMBER_DISCOUNTS.get(memberType, Decimal("1.0"))


def applyCouponDiscount(price, couponCode):
    return price * COUPON_DISCOUNTS.get(couponCode, Decimal("1.0"))


FREE_DELIVERY_THRESHOLD = Decimal(100)
DELIVERY_COST = Decimal(12)


def applyDeliveryCost(price):
    if price < FREE_DELIVERY_THRESHOLD:
        price += DELIVERY_COST
    return price


TAXES_PERCENTAGE = Decimal("0.23")


def applyTaxes(price):
    return price * (1 + TAXES_PERCENTAGE)


if __name__ == "__main__":
    processor = OrderProcessor()

    handleCommand(processor, "ORDER Alice|alice@example.test|VIP|BOOK:2,PEN:3|SAVE10")
    handleCommand(processor, "ORDER Bob|bob@example.test|REGULAR|BAG:2|NONE")
    handleCommand(processor, "REPORT")

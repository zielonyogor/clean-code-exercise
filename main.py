from pathlib import Path
from enum import Enum
from decimal import Decimal
from dataclasses import dataclass


class MemberType(Enum):
    REGULAR = 1
    VIP = 2
    STUDENT = 3


PRODUCT_PRICE = {
    "BOOK": Decimal(40),
    "PEN": Decimal(5),
    "BAG": Decimal(80),
}

MEMBER_DISCOUNTS = {
    MemberType.REGULAR: Decimal("1.0"),
    MemberType.VIP: Decimal("0.9"),
    MemberType.STUDENT: Decimal("0.95"),
}

COUPON_DISCOUNTS = {
    "SAVE10": Decimal("0.9"),
}

FREE_DELIVERY_THRESHOLD = Decimal(100)
DELIVERY_COST = Decimal(12)
TAXES_PERCENTAGE = Decimal("0.23")


def getProductPrice(product):
    return PRODUCT_PRICE.get(product, 0)


@dataclass
class OrderLine:
    product: str
    quantity: int

    def getPrice(self):
        return getProductPrice(self.product) * self.quantity

    def __str__(self):
        return f"{self.product}x{self.quantity};"


@dataclass
class Order:
    name: str
    email: str
    memberType: MemberType
    lines: list[OrderLine]
    couponCode: str

    def getSubtotal(self):
        return sum(line.getPrice() for line in self.lines)

    def describeProducts(self):
        return "".join(str(line) for line in self.lines)


def parseOrder(orderStringRepresentation):
    orderInformation = orderStringRepresentation.split("|")
    return Order(
        name=orderInformation[0],
        email=orderInformation[1],
        memberType=MemberType[orderInformation[2]],
        lines=parseOrderLines(orderInformation[3]),
        couponCode=orderInformation[4],
    )


def parseOrderLines(productsStringRepresentation):
    lines = []
    for productWithQuantity in productsStringRepresentation.split(","):
        product, quantityStr = productWithQuantity.split(":")
        lines.append(OrderLine(product, int(quantityStr)))
    return lines


class FileOrderRepository:
    def __init__(self, path):
        self.path = path

    def save(self, orderDescription):
        with self.path.open("a", encoding="utf-8") as f:
            f.write(orderDescription + "\n")


class ConsoleNotifier:
    def send(self, email, message):
        print("EMAIL " + email + "|" + message)


class OrderProcessor:
    def __init__(self, repository, notifier):
        self.repository = repository
        self.notifier = notifier
        self.counter = 0
        self.total = 0

    def order(self, orderInformationString, verbose=True):
        order = parseOrder(orderInformationString)
        price = calculatePrice(order)
        orderDescription = f"ORDER|{order.name}|{order.describeProducts()}|{price:.2f}"
        self.counter += 1
        self.total += price

        try:
            self.repository.save(orderDescription)
            self.notifier.send(order.email, orderDescription)
            if verbose:
                print(orderDescription)
            return orderDescription
        except Exception:
            return "ERROR"

    def report(self):
        print(f"REPORT|{self.counter}|{self.total:.2f}")


def calculatePrice(order):
    price = order.getSubtotal()
    price = applyMemberDiscount(price, order.memberType)
    price = applyCouponDiscount(price, order.couponCode)
    price = applyDeliveryCost(price)
    return applyTaxes(price)


def handleCommand(processor, commandLine):
    command, _, payload = commandLine.partition(" ")
    if command == "ORDER":
        return processor.order(payload)
    if command == "REPORT":
        return processor.report()
    return "UNKNOWN"


def applyMemberDiscount(price, memberType):
    return price * MEMBER_DISCOUNTS.get(memberType, Decimal("1.0"))


def applyCouponDiscount(price, couponCode):
    return price * COUPON_DISCOUNTS.get(couponCode, Decimal("1.0"))


def applyDeliveryCost(price):
    if price < FREE_DELIVERY_THRESHOLD:
        price += DELIVERY_COST
    return price


def applyTaxes(price):
    return price * (1 + TAXES_PERCENTAGE)


if __name__ == "__main__":
    processor = OrderProcessor(FileOrderRepository(Path("orders.txt")), ConsoleNotifier())

    handleCommand(processor, "ORDER Alice|alice@example.test|VIP|BOOK:2,PEN:3|SAVE10")
    handleCommand(processor, "ORDER Bob|bob@example.test|REGULAR|BAG:2|NONE")
    handleCommand(processor, "REPORT")

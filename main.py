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


def get_product_price(product):
    return PRODUCT_PRICE.get(product, 0)


@dataclass
class OrderLine:
    product: str
    quantity: int

    def get_price(self):
        return get_product_price(self.product) * self.quantity

    def __str__(self):
        return f"{self.product}x{self.quantity};"


@dataclass
class Order:
    name: str
    email: str
    member_type: MemberType
    lines: list[OrderLine]
    coupon_code: str

    def get_subtotal(self):
        return sum(line.get_price() for line in self.lines)

    def describe_products(self):
        return "".join(str(line) for line in self.lines)


def parse_order(order_text):
    order_information = order_text.split("|")
    return Order(
        name=order_information[0],
        email=order_information[1],
        member_type=MemberType[order_information[2]],
        lines=parse_order_lines(order_information[3]),
        coupon_code=order_information[4],
    )


def parse_order_lines(products_text):
    lines = []
    for product_with_quantity in products_text.split(","):
        product, quantity_text = product_with_quantity.split(":")
        lines.append(OrderLine(product, int(quantity_text)))
    return lines


class FileOrderRepository:
    def __init__(self, path):
        self.path = path

    def save(self, order_description):
        with self.path.open("a", encoding="utf-8") as f:
            f.write(order_description + "\n")


class ConsoleNotifier:
    def send(self, email, message):
        print("EMAIL " + email + "|" + message)


class OrderProcessor:
    def __init__(self, repository, notifier):
        self.repository = repository
        self.notifier = notifier
        self.counter = 0
        self.total = 0

    def order(self, order_text):
        order = parse_order(order_text)
        price = calculate_price(order)
        order_description = f"ORDER|{order.name}|{order.describe_products()}|{price:.2f}"

        try:
            self.repository.save(order_description)
        except OSError:
            return "ERROR"

        self.counter += 1
        self.total += price
        self.notifier.send(order.email, order_description)
        return order_description

    def report(self):
        return f"REPORT|{self.counter}|{self.total:.2f}"


def calculate_price(order):
    price = order.get_subtotal()
    price = apply_member_discount(price, order.member_type)
    price = apply_coupon_discount(price, order.coupon_code)
    price = apply_delivery_cost(price)
    return apply_taxes(price)


def handle_command(processor, command_line):
    command, _, payload = command_line.partition(" ")
    if command == "ORDER":
        return processor.order(payload)
    if command == "REPORT":
        return processor.report()
    return "UNKNOWN"


def apply_member_discount(price, member_type):
    return price * MEMBER_DISCOUNTS.get(member_type, Decimal("1.0"))


def apply_coupon_discount(price, coupon_code):
    return price * COUPON_DISCOUNTS.get(coupon_code, Decimal("1.0"))


def apply_delivery_cost(price):
    if price < FREE_DELIVERY_THRESHOLD:
        price += DELIVERY_COST
    return price


def apply_taxes(price):
    return price * (1 + TAXES_PERCENTAGE)


if __name__ == "__main__":
    processor = OrderProcessor(FileOrderRepository(Path("orders.txt")), ConsoleNotifier())

    print(handle_command(processor, "ORDER Alice|alice@example.test|VIP|BOOK:2,PEN:3|SAVE10"))
    print(handle_command(processor, "ORDER Bob|bob@example.test|REGULAR|BAG:2|NONE"))
    print(handle_command(processor, "REPORT"))

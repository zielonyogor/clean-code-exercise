# Changelog and Decisions

## Removed code

We removed every code that was not used or was not providing any value.

| Code | Reason |
|------|--------|
| class Everything | an interface that was not providing any value |
| refund() method | neither implemented nor used in main |
| `future_currencies` | a variable that was not used |
| `mode` | a variable that was not used |
| `cache` | a variable that was not used |
| parameter `unused` in method `doIt()` | a variable that was not used |

## Naming

We improved the naming of variables and methods to better reflect their purpose and usage.

| Old Name | New Name |
|----------|----------|
| class `Thing` | `Order` |
| `doIt()` | `order()` and `showReport()` |
| `a` | `orderInformation`|
| `z` | `price` |
| `p` | `PRODUCT_PRICE` |
| `t` | `MemberType` |

## Magic numbers

We replaced magic numbers with named constants to improve code readability and maintainability.

| Old Value | New Constant |
|-----------|-------------|
| 100 | `FREE_DELIVERY_THRESHOLD` |
| 12 | `DELIVERY_COST` |
| 23% | `TAXES_PERCENTAGE` |
| 40, 5, 8 | `PRODUCT_PRICE` |
| 1, 2 | `Action(Enum): ORDER, REPORT` |
| 1, 2, 3 | `MemberType(Enum): REGULAR, VIP, STUDENT` |
| 0.9, 0.9, 0.85 | `DISCOUNTS` |

## Class and functions extraction

We extracted classes and functions to improve code organization and readability.

### New classes

* `class ProductsHolder`: a class responsible for holding and managing product information; currently the only purpose is to provide total price and return string with list of products
* `class OrderDetails`: data class for holding information about order, such as name, email, etc.
* `class OrderProcessor`: processor class responsible for executing different actions:
  - `processOrder()`: processes the order based on the provided order details and products
  - `generateReport()`: generates a report for the processed order

## Functions extraction

We extracted functions to improve code organization and readability.

* `getProductPrice()`: returns the price of a product from `PRODUCT_PRICE`
* `applyDiscount()`: applies a discount based on member type or discount code from `DISCOUNTS`
* `applyDeliveryCost()`: adds `DELIVERY_COST` when the price is below `FREE_DELIVERY_THRESHOLD`
* `applyTaxes()`: adds `TAXES_PERCENTAGE` to the price
* `executeAction()`: runs the given `Action` instead of checking magic numbers in `doIt()`

## Global state

We removed global variables `counter` and `total`; they are now fields of `OrderProcessor`.

## Money precision

We replaced `float` with `Decimal` for prices, discounts, delivery cost and taxes to avoid floating point errors in money calculations.

## Further cleanup

We removed the leftovers of the previous steps and simplified the code.

| Change | Reason |
|--------|--------|
| removed commented-out class `Everything` | commented-out code is still dead code |
| removed `refund()` method | neither implemented nor used |
| `DISCOUNTS` split into `MEMBER_DISCOUNTS` and `COUPON_DISCOUNTS` | member types and coupons are different concepts |
| `applyDiscount()` split into `applyMemberDiscount()` and `applyCouponDiscount()` | each function applies one kind of discount |
| default values for `verbose`, `send`, `save` | callers no longer pass `True, True, True` |
| `executeAction()` moved out of `OrderProcessor` as `handleCommand()` | command handling is separated from order logic; streaming input can still call operations generically |
| `Action(Enum)` replaced with text commands `ORDER <order line>` and `REPORT` | commands can be read directly from input |

### Naming

| Old Name | New Name |
|----------|----------|
| `obj` | `order` |
| `x` | `message`, `orderDescription` |
| `detail` | `productsDescription` |
| `_order()` | `order()` |
| `_showReport()` | `report()` |

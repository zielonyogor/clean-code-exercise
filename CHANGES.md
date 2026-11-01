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

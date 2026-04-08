---
name: No circular imports
description: Modules must not create circular import dependencies between packages
type: rule
scope: "src/**/*.py"
severity: warn
---

## Intent

Circular imports cause initialization failures, make dependency graphs
unpredictable, and signal that module boundaries are poorly defined.
Dependencies should flow in one direction — typically from higher-level
modules toward lower-level ones.

## Non-Compliant Example

```python
# src/services/order.py
from src.services.payment import process_payment  # depends on payment

class OrderService:
    def complete(self, order):
        process_payment(order.total)
```

```python
# src/services/payment.py
from src.services.order import OrderService  # depends on order — circular!

class PaymentProcessor:
    def refund(self, payment):
        order = OrderService.find(payment.order_id)
```

Violation: `order` imports `payment` and `payment` imports `order`,
creating a circular dependency.

## Compliant Example

```python
# src/services/order.py
from src.services.payment import process_payment

class OrderService:
    def complete(self, order):
        process_payment(order.total)
```

```python
# src/services/payment.py
# No import of order — breaks the cycle
# Uses order_id (a primitive) instead of the OrderService class

class PaymentProcessor:
    def refund(self, payment):
        # Accept order_id as a parameter instead of importing OrderService
        return RefundResult(order_id=payment.order_id)
```

Dependency flows one direction: orders depend on payments, payments
do not depend on orders.

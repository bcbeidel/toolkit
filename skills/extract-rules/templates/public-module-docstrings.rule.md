---
name: Public module docstrings
description: Public-facing modules must have a module-level docstring explaining their purpose
type: rule
scope: "src/**/*.py"
severity: warn
---

## Intent

Module docstrings are the first thing a developer reads when navigating
to a file. Without them, developers must read the entire module to
understand its purpose, increasing onboarding time and making the
codebase harder to navigate.

## Non-Compliant Example

```python
# src/services/billing.py
import stripe
from datetime import datetime

class BillingService:
    def charge(self, customer_id, amount):
        ...
```

Violation: no module-level docstring. A developer arriving at this file
must read the class and method signatures to infer the module's purpose.

## Compliant Example

```python
# src/services/billing.py
"""Billing service for processing customer charges and refunds.

Wraps the Stripe API for payment processing. Used by the order
completion flow and the admin refund interface.
"""

import stripe
from datetime import datetime

class BillingService:
    def charge(self, customer_id, amount):
        ...
```

The module docstring immediately communicates purpose, dependencies,
and usage context.

---
name: Test file required for new modules
description: Every production module must have a corresponding test file
type: rule
scope: "src/**/*.py"
severity: warn
---

## Intent

Modules without tests accumulate technical debt silently. Requiring a
test file at creation time is far cheaper than retrofitting tests later,
and ensures new code has at least a basic verification path.

## Non-Compliant Example

```
src/
  services/
    payment.py        # new module
tests/
  services/
    # no test_payment.py — violation
```

A new module exists in `src/` with no corresponding test file in `tests/`.

## Compliant Example

```
src/
  services/
    payment.py
tests/
  services/
    test_payment.py   # corresponding test file exists
```

Every module in `src/` has a mirrored test file in `tests/` with the
`test_` prefix.

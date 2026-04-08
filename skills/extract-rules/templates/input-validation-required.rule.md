---
name: Input validation required
description: API endpoint handlers must validate input before processing
type: rule
scope: "src/api/**/*.py"
severity: warn
---

## Intent

Unvalidated input is the root cause of injection attacks, data corruption,
and hard-to-debug runtime errors. Validating at the API boundary catches
bad data before it propagates through the system.

## Non-Compliant Example

```python
# src/api/users.py
@app.post("/users")
def create_user(request):
    # No validation — raw input goes directly to the database
    db.execute(
        "INSERT INTO users (name, email) VALUES (?, ?)",
        request.json["name"],
        request.json["email"]
    )
    return {"status": "created"}
```

Violations: no type checking, no required field validation, no format
validation on email. Raw input flows directly to the database.

## Compliant Example

```python
# src/api/users.py
from pydantic import BaseModel, EmailStr

class CreateUserRequest(BaseModel):
    name: str
    email: EmailStr

@app.post("/users")
def create_user(request):
    body = CreateUserRequest(**request.json)  # validates input
    db.execute(
        "INSERT INTO users (name, email) VALUES (?, ?)",
        body.name,
        body.email
    )
    return {"status": "created"}
```

Input is validated against a schema before processing. Invalid requests
fail fast with clear error messages.

---
name: No hardcoded secrets
description: Source files must not contain hardcoded credentials, API keys, or connection strings
type: rule
scope:
  - "src/**/*.py"
  - "src/**/*.ts"
  - "src/**/*.js"
severity: fail
---

## Intent

Hardcoded secrets in source code get committed to version control,
shared across environments, and are difficult to rotate. Secrets
must come from environment variables, secret managers, or configuration
files excluded from version control.

## Non-Compliant Example

```python
# src/services/database.py
import psycopg2

conn = psycopg2.connect(
    host="prod-db.internal.example.com",
    password="s3cret_p@ssw0rd",         # hardcoded credential
    dbname="production"
)

API_KEY = "sk-abc123def456ghi789"        # hardcoded API key
```

Violations: database password and API key are embedded directly in
source code.

## Compliant Example

```python
# src/services/database.py
import os
import psycopg2

conn = psycopg2.connect(
    host=os.environ["DB_HOST"],
    password=os.environ["DB_PASSWORD"],   # from environment
    dbname=os.environ["DB_NAME"]
)

API_KEY = os.environ["API_KEY"]           # from environment
```

All sensitive values come from environment variables. No secrets
appear in source code.

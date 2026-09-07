# Day 003 — Preventing SQL Injection with Parameterized Queries

## Overview

One of the most important backend security rules is:

> User-controlled data must never become executable SQL.

Building SQL queries through string concatenation can create SQL Injection vulnerabilities.

---

## Unsafe Approach

```ts
async function getUserByEmail(email: string) {
  return db.query(`
    SELECT *
    FROM Users
    WHERE Email = '${email}'
  `);
}
```

The application mixes SQL syntax and user-controlled data inside the same string.

---

## Parameterized Query

Using SQL Server:

```ts
import sql from "mssql";

interface User {
  userId: number;
  name: string;
  email: string;
}

async function getUserByEmail(
  email: string
): Promise<User | null> {
  const pool = await sql.connect(
    process.env.DB_CONNECTION!
  );

  const result = await pool
    .request()
    .input(
      "email",
      sql.NVarChar(320),
      email
    )
    .query<User>(`
      SELECT
        UserId AS userId,
        Name AS name,
        Email AS email
      FROM Users
      WHERE Email = @email
    `);

  return result.recordset[0] ?? null;
}
```

The SQL statement and the parameter value are now handled separately.

```text
SQL Statement
     +
Parameter Values
     ↓
Database Driver
     ↓
SQL Server
```

---

## Validation Is Not Parameterization

Input validation is still useful:

```text
HTTP Request
     ↓
Validation
     ↓
Business Logic
     ↓
Parameterized Query
     ↓
Database
```

However, validating an email or trimming a string does not replace parameterized queries.

Each layer solves a different problem.

---

## Dynamic Identifiers

Values should use parameters.

Dynamic identifiers such as sort columns should normally use strict allowlists.

```ts
const allowedColumns = [
  "Name",
  "Email",
  "CreatedTime",
] as const;
```

Never blindly insert user-controlled identifiers into SQL.

General rule:

```text
Values
→ Parameters

Dynamic identifiers
→ Strict Allowlist
```

---

## Better Backend Architecture

Avoid placing SQL directly inside controllers.

Prefer:

```text
HTTP Request
     ↓
Controller
     ↓
Service
     ↓
Repository
     ↓
Database
```

Example:

```ts
class UserRepository {
  constructor(
    private readonly pool: sql.ConnectionPool
  ) {}

  async findByEmail(
    email: string
  ): Promise<User | null> {
    const result = await this.pool
      .request()
      .input(
        "email",
        sql.NVarChar(320),
        email
      )
      .query<User>(`
        SELECT
          UserId AS userId,
          Name AS name,
          Email AS email
        FROM Users
        WHERE Email = @email
      `);

    return result.recordset[0] ?? null;
  }
}
```

---

## AI Engineering Connection

Allowing an LLM or AI agent to generate unrestricted SQL against a production database creates a dangerous trust boundary.

Avoid architectures like:

```text
User
 ↓
LLM
 ↓
Generated SQL
 ↓
Production Database
```

Prefer:

```text
User
 ↓
LLM
 ↓
Structured Intent
 ↓
Validation
 ↓
Approved Tool
 ↓
Parameterized Repository
 ↓
Database
```

Instead of generating raw SQL, an AI system could produce:

```json
{
  "action": "find_user",
  "email": "user@example.com"
}
```

The application then maps that request to a controlled function:

```ts
repository.findByEmail(input.email);
```

This gives the model access to a narrow capability instead of unrestricted database execution.

---

## Exercise

Create:

```ts
findByPriceRange(
  minPrice: number,
  maxPrice: number
)
```

for a property repository.

Use:

```sql
SELECT
  Id,
  Title,
  Price
FROM Properties
WHERE Price BETWEEN @minPrice AND @maxPrice
```

Both values must be parameterized.

### Bonus

Support sorting using only:

- `Price`
- `CreatedTime`
- `Title`

Implement the sort field using a strict allowlist.

---

## Interview Question

### How do you prevent SQL Injection?

Use parameterized queries or prepared statements so user-controlled values are never concatenated into SQL.

For dynamic identifiers such as column names, use a strict allowlist.

---

## Key Takeaways

- Never concatenate user input into SQL.
- Use parameterized queries for values.
- Validation does not replace parameterization.
- Use allowlists for dynamic identifiers.
- Keep database access behind a repository layer.
- Never give AI agents unrestricted database execution.

## Daily Engineering Principle

> Keep data as data — never let user-controlled input become executable SQL.
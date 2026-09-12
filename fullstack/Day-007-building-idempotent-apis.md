# Day 007 — Building Idempotent APIs for Safe Retries

## Overview

Distributed systems experience retries.

A client may send a request successfully while failing to receive the response.

If the client retries a non-idempotent operation, the same logical action may execute multiple times.

Examples include:

- payment creation
- order creation
- sending messages
- CRM activity creation
- AI tool execution

---

## The Problem

```ts
app.post("/api/calls", async (req, res) => {
  const call =
    await callRepository.create(
      req.body
    );

  return res
    .status(201)
    .json(call);
});
```

Consider this sequence:

```text
Request
   ↓
Call Created
   ↓
Response Lost
   ↓
Client Retries
   ↓
Another Call Created
```

One logical operation created two side effects.

---

## Idempotency Keys

The client creates an identifier for the logical operation:

```ts
const idempotencyKey =
  crypto.randomUUID();
```

Then sends it with the request:

```ts
await fetch("/api/calls", {
  method: "POST",

  headers: {
    "Content-Type":
      "application/json",

    "Idempotency-Key":
      idempotencyKey,
  },

  body: JSON.stringify({
    customerId: 42,
    description:
      "Customer requested a follow-up.",
  }),
});
```

Retries must reuse the same key.

```text
Logical Operation
       ↓
Idempotency Key
       ↓
Attempt 1
Attempt 2
Attempt 3
```

---

## Server Flow

```text
Request
   ↓
Idempotency Key
   ↓
Previously processed?
   │
   ├── Yes
   │     ↓
   │ Return previous result
   │
   └── No
         ↓
      Execute
         ↓
      Store result
         ↓
      Response
```

Example service:

```ts
class CallService {
  constructor(
    private readonly calls:
      CallRepository,

    private readonly idempotency:
      IdempotencyRepository
  ) {}

  async createCall(
    key: string,
    input: CreateCallInput
  ) {
    const existing =
      await this.idempotency.find(
        key
      );

    if (existing) {
      return existing.response;
    }

    const call =
      await this.calls.create(
        input
      );

    await this.idempotency.save({
      key,
      response: call,
    });

    return call;
  }
}
```

---

## Concurrency Problem

A simple check is not sufficient.

Two requests can execute concurrently:

```text
Request A → key not found
Request B → key not found

Request A → create
Request B → create
```

This is a race condition.

The database should enforce uniqueness.

```sql
CREATE TABLE IdempotencyKeys (
    Id BIGINT IDENTITY PRIMARY KEY,

    IdempotencyKey
        NVARCHAR(100) NOT NULL,

    ResponseBody
        NVARCHAR(MAX) NULL,

    CreatedAt
        DATETIME2 NOT NULL
        DEFAULT SYSUTCDATETIME(),

    CONSTRAINT UQ_IdempotencyKey
        UNIQUE (IdempotencyKey)
);
```

Application checks improve behavior.

Database constraints enforce invariants.

---

## Scope the Key

In multi-user systems, keys may be scoped using:

```text
UserId
+
IdempotencyKey
```

or:

```text
UserId
+
Endpoint
+
IdempotencyKey
```

depending on the API design.

---

## Request Fingerprints

A client should not reuse the same key for different operations.

Store a hash of the request payload:

```ts
import crypto from "node:crypto";

function createRequestHash(
  payload: unknown
): string {
  return crypto
    .createHash("sha256")
    .update(
      JSON.stringify(payload)
    )
    .digest("hex");
}
```

Then enforce:

```text
Same Key
+
Same Request Hash
→ Return previous result
```

while:

```text
Same Key
+
Different Request Hash
→ Reject
```

This can be returned as a conflict response.

---

## Transactions

Consider:

```text
Business Operation Succeeded
          ↓
Idempotency Record Failed
```

A retry may execute the business operation again.

Where possible, coordinate the business write and idempotency state transactionally:

```text
BEGIN

Business Write

Idempotency Record

COMMIT
```

On failure:

```text
ROLLBACK
```

---

## AI Agent Connection

Idempotency is especially important for AI tools with side effects.

Imagine:

```ts
createPayment({
  customerId: 42,
  amount: 500000,
});
```

If the agent runtime retries the tool after a network failure, the payment must not be created twice.

A safer flow is:

```text
Agent
 ↓
Tool Call ID
 ↓
Idempotency Layer
 ↓
Already executed?
 ↓
Yes → Previous result
No  → Execute tool
```

A tool can carry a stable operation identifier:

```ts
interface PaymentToolInput {
  operationId: string;
  customerId: number;
  amount: number;
}
```

The application maps that identifier to its idempotency mechanism.

> AI retries must not multiply real-world side effects.

---

## HTTP Semantics

Methods such as:

```text
GET
PUT
DELETE
```

are intended to have idempotent semantics.

`POST`, however, is not inherently idempotent.

For example:

```http
POST /orders
```

may create a new order each time.

Sensitive POST operations often benefit from explicit idempotency support.

---

## Exercise

Design an idempotent endpoint:

```http
POST /api/payments
```

Input:

```ts
interface CreatePaymentInput {
  userId: number;
  amount: number;
}
```

Requirements:

1. Generate one operation ID per logical payment.
2. Reuse it across retries.
3. Store the idempotency key with a database uniqueness constraint.
4. Store a request fingerprint.
5. Reject the same key with a different payload.
6. Coordinate payment creation and idempotency state transactionally.

### Bonus

Design an expiration policy for old idempotency records appropriate to the operation.

---

## Interview Question

### What is idempotency in APIs?

Idempotency means retrying the same logical operation does not create unintended duplicate side effects.

For operations such as payments or order creation, an idempotency key can identify the logical operation, while persisted results and database uniqueness allow retries to safely return the previous outcome.

### Is checking the key before insertion enough?

No.

A check-then-insert flow can race under concurrency. Database uniqueness and atomic or transactional handling are needed to enforce the invariant reliably.

---

## Key Takeaways

- Network retries are normal.
- Logical operations need stable identities.
- Reuse the same idempotency key across retries.
- Store previous outcomes when appropriate.
- Enforce uniqueness in the database.
- Protect against key reuse with different payloads.
- Think about concurrency, not only sequential requests.
- AI tools with side effects also need retry safety.

## Daily Engineering Principle

> Design every important side effect as if the network will retry it.
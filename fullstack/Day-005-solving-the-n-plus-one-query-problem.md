# Day 005 — Solving the N+1 Query Problem

## Overview

The N+1 query problem is one of the most common database performance issues in backend applications.

It happens when an application loads a collection using one query and then executes another query for every item.

---

## The Problem

```ts
const agencies = await db.query(`
  SELECT Id, Name
  FROM Agencies
`);

for (const agency of agencies) {
  const result = await db.query(`
    SELECT COUNT(*) AS Count
    FROM Users
    WHERE AgencyId = ${agency.Id}
  `);

  agency.consultantCount =
    result[0].Count;
}
```

For 100 agencies:

```text
1 initial query
+
100 additional queries
=
101 database queries
```

This creates unnecessary database round trips.

---

## Think in Sets

Relational databases are optimized for set-based operations.

Instead of querying each agency separately:

```sql
SELECT
    a.Id,
    a.Name,
    COUNT(u.UserId) AS ConsultantCount

FROM Agencies a

LEFT JOIN Users u
    ON u.AgencyId = a.Id

GROUP BY
    a.Id,
    a.Name;
```

Now the database can return the result with one query.

```text
N + 1 Queries

↓

1 Set-Based Query
```

---

## Why LEFT JOIN?

`LEFT JOIN` keeps agencies that do not currently have any users.

```json
{
  "id": 7,
  "name": "New Agency",
  "consultantCount": 0
}
```

Using:

```sql
COUNT(u.UserId)
```

ensures null joined rows are not counted.

---

## Repository Example

```ts
interface AgencyReport {
  id: number;
  name: string;
  consultantCount: number;
}

class AgencyRepository {
  async getReports():
    Promise<AgencyReport[]> {

    return db.query(`
      SELECT
        a.Id AS id,
        a.Name AS name,
        COUNT(u.UserId)
          AS consultantCount

      FROM Agencies a

      LEFT JOIN Users u
        ON u.AgencyId = a.Id

      GROUP BY
        a.Id,
        a.Name

      ORDER BY
        consultantCount DESC
    `);
  }
}
```

---

## JOIN Is Not the Only Solution

Depending on the problem, useful techniques include:

- JOIN
- Batch queries
- Aggregation
- Eager loading
- DataLoader
- Caching

Example batch lookup:

```sql
SELECT
    Id,
    Name
FROM Agencies
WHERE Id IN (1, 4, 7, 12);
```

Instead of:

```text
100 individual lookups
```

perform:

```text
1 batch lookup
```

---

## Watch Your ORM

Clean ORM code can still generate inefficient SQL.

```ts
const agencies =
  await orm.agency.findMany();

for (const agency of agencies) {
  agency.users =
    await orm.user.findMany({
      where: {
        agencyId: agency.id,
      },
    });
}
```

Always understand how your ORM accesses the database.

> Clean application code does not automatically mean efficient database access.

---

## Detecting N+1

A suspicious query log may look like:

```text
SELECT * FROM Agencies

SELECT * FROM Users WHERE AgencyId = 1
SELECT * FROM Users WHERE AgencyId = 2
SELECT * FROM Users WHERE AgencyId = 3
SELECT * FROM Users WHERE AgencyId = 4
...
```

Useful tools include:

- Query logging
- Distributed tracing
- APM
- Database monitoring
- Slow-query analysis

---

## Indexing

If a relationship is frequently queried:

```sql
Users.AgencyId
```

an index may improve access:

```sql
CREATE INDEX IX_Users_AgencyId
ON Users (AgencyId);
```

Indexes are not free.

They can improve reads but increase:

- storage usage
- insert cost
- update cost

Measure before optimizing.

---

## AI Engineering Connection

The same principle appears in AI systems.

Avoid:

```ts
for (const document of documents) {
  await createEmbedding(document);
}
```

when the provider supports batching.

Prefer:

```ts
await createEmbeddings(
  documents.map(
    document => document.content
  )
);
```

Conceptually:

```text
Repeated Remote Calls
        ↓
Batch Work
        ↓
Lower Overhead
```

This is especially useful in embedding pipelines and RAG ingestion systems.

---

## Exercise

Assume:

```text
Properties
PropertyImages
```

A property can contain multiple images.

Bad implementation:

```ts
const properties =
  await getProperties();

for (const property of properties) {
  property.images =
    await getImages(property.id);
}
```

For 50 properties this can create:

```text
51 queries
```

Refactor the implementation using either:

1. JOIN
2. Batch query

Example:

```sql
SELECT *
FROM PropertyImages
WHERE PropertyId IN (...);
```

Then group images by `PropertyId` in the application.

---

## Interview Question

### What is the N+1 query problem?

The N+1 problem occurs when an application loads a collection using one query and then executes an additional query for each item.

Common solutions include set-based queries, joins, eager loading, batching, and DataLoader-style patterns.

When using an ORM, inspect the generated SQL instead of assuming database access is efficient.

---

## Key Takeaways

- Minimize database round trips.
- Prefer set-based operations.
- Watch for hidden N+1 behavior in ORMs.
- Batch related lookups when appropriate.
- Use indexes based on actual query patterns.
- Measure before optimizing.
- The batching principle also applies to AI workloads.

## Daily Engineering Principle

> Optimize the number of round trips, not just the speed of each individual operation.
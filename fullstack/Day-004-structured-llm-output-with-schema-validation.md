# Day 004 — Reliable LLM Structured Output with Schema Validation

## Overview

LLMs are excellent at generating text, but production applications usually need predictable data.

For example, a user might say:

```text
I need a two-bedroom apartment in Tehran
under 8 billion.
```

The application may need:

```json
{
  "city": "Tehran",
  "propertyType": "apartment",
  "bedrooms": 2,
  "minPrice": null,
  "maxPrice": 8000000000
}
```

This is where structured output becomes important.

---

## The Problem with Free-Form Output

A fragile implementation might look like:

```ts
async function extractFilters(
  message: string
) {
  const response = await llm.generate(`
    Extract property filters.
    Return JSON.

    ${message}
  `);

  return JSON.parse(response);
}
```

Several things can go wrong:

- The model may include additional text.
- The JSON may be malformed.
- Required fields may be missing.
- Numbers may be returned as strings.
- Unsupported enum values may appear.
- Syntactically valid JSON may still violate business rules.

---

## Define a Schema

```ts
import { z } from "zod";

const PropertySearchSchema = z.object({
  city: z.string().nullable(),

  propertyType: z
    .enum([
      "apartment",
      "villa",
      "office",
      "land",
    ])
    .nullable(),

  bedrooms: z
    .number()
    .int()
    .min(0)
    .nullable(),

  minPrice: z
    .number()
    .nonnegative()
    .nullable(),

  maxPrice: z
    .number()
    .nonnegative()
    .nullable(),
});

type PropertySearch =
  z.infer<typeof PropertySearchSchema>;
```

The schema becomes a contract between the AI layer and the application.

---

## Validate AI Output

```ts
async function extractPropertyFilters(
  message: string
): Promise<PropertySearch> {
  const rawOutput: unknown =
    await generateStructuredOutput({
      input: message,
      schema: PropertySearchSchema,
    });

  const result =
    PropertySearchSchema.safeParse(
      rawOutput
    );

  if (!result.success) {
    throw new Error(
      "Invalid AI output"
    );
  }

  return result.data;
}
```

Until validation succeeds, AI output should be considered untrusted.

```text
User
 ↓
LLM
 ↓
Untrusted Output
 ↓
Schema Validation
 ↓
Trusted Domain Object
 ↓
Application
```

---

## Add Business Validation

Correct types do not necessarily mean correct business logic.

For example:

```json
{
  "minPrice": 9000000000,
  "maxPrice": 5000000000
}
```

Both values are valid numbers, but the range is invalid.

Use schema refinement:

```ts
const PropertySearchSchema = z
  .object({
    city: z.string().nullable(),

    propertyType: z
      .enum([
        "apartment",
        "villa",
        "office",
        "land",
      ])
      .nullable(),

    bedrooms: z
      .number()
      .int()
      .min(0)
      .nullable(),

    minPrice: z
      .number()
      .nonnegative()
      .nullable(),

    maxPrice: z
      .number()
      .nonnegative()
      .nullable(),
  })
  .refine(
    (data) => {
      if (
        data.minPrice === null ||
        data.maxPrice === null
      ) {
        return true;
      }

      return data.minPrice <= data.maxPrice;
    },
    {
      message:
        "minPrice cannot be greater than maxPrice",
    }
  );
```

A production system often needs both:

```text
Structural Validation
        +
Domain Validation
```

---

## Keep the LLM Away from Infrastructure

Avoid:

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
Application Service
 ↓
Repository
 ↓
Parameterized Query
 ↓
Database
```

The model should describe what needs to happen.

The application should control how it happens.

---

## Structured Tool Calls

Instead of allowing an AI agent to create arbitrary database commands, define narrow tools.

Example output:

```json
{
  "tool": "get_user",
  "arguments": {
    "userId": 42
  }
}
```

Validate it:

```ts
const ToolCallSchema = z.object({
  tool: z.literal("get_user"),

  arguments: z.object({
    userId: z
      .number()
      .int()
      .positive(),
  }),
});
```

Then execute controlled application code:

```ts
const result =
  ToolCallSchema.safeParse(aiOutput);

if (!result.success) {
  throw new Error(
    "Invalid tool call"
  );
}

await getUser(
  result.data.arguments.userId
);
```

A useful design principle is:

```text
LLM decides WHAT
Application decides HOW
```

---

## Prompting Is Not Validation

This instruction:

```text
Return only valid JSON.
```

can improve model behavior, but it is not a security boundary.

```text
Prompt Instructions
       ≠
Runtime Validation
```

Always validate data before it affects application state, infrastructure, or tools.

---

## Exercise

Build a CRM intent extractor.

Example user request:

```text
Show the call history for customer
09121234567.
```

Start with:

```ts
const CRMIntentSchema = z.object({
  action: z.enum([
    "find_customer",
    "get_call_history",
    "create_call",
  ]),

  phoneNumber: z
    .string()
    .nullable(),

  customerId: z
    .number()
    .int()
    .positive()
    .nullable(),
});
```

Requirements:

1. Infer the TypeScript type with `z.infer`.
2. Create `extractCRMIntent()`.
3. Treat AI output as `unknown`.
4. Validate it using `safeParse()`.
5. Require either `phoneNumber` or `customerId` when retrieving call history.
6. Never expose unrestricted SQL execution to the model.

### Bonus

Implement requirement 5 using `.refine()`.

---

## Interview Question

### Why shouldn't you trust JSON generated by an LLM?

Valid JSON guarantees syntax, not correctness.

LLM output should be constrained with a schema and runtime-validated before it enters application logic or triggers tools.

For AI agents, a strong architecture lets the model produce structured intent or tool arguments while the application retains control over validation, authorization, and execution.

---

## Key Takeaways

- Treat LLM output as untrusted external data.
- Prefer structured output over free-form parsing.
- Validate structured output at runtime.
- Add domain validation beyond basic type validation.
- Prompts are not security boundaries.
- Give AI agents narrow tools instead of unrestricted infrastructure access.
- Keep authorization and execution under application control.

## Daily Engineering Principle

> Let the model suggest intent; let deterministic application code validate and execute it.
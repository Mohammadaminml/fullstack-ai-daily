# Day 008 — Building Optimistic UI with React

## Overview

Traditional interfaces wait for the server before updating the UI.

```text
User Action
    ↓
API Request
    ↓
Server Response
    ↓
Update UI
```

Optimistic UI changes the interface immediately and reconciles the result afterward.

```text
User Action
    ↓
Optimistic Update
    ↓
API Request
    ↓
Success → Keep State
Failure → Rollback
```

This can dramatically improve perceived performance.

---

## A Slow Approach

```tsx
const handleComplete = async () => {
  setLoading(true);

  const response = await fetch(
    `/api/calls/${call.id}`,
    {
      method: "PATCH",

      headers: {
        "Content-Type":
          "application/json",
      },

      body: JSON.stringify({
        status: "completed",
      }),
    }
  );

  if (response.ok) {
    setCall({
      ...call,
      status: "completed",
    });
  }

  setLoading(false);
};
```

The interface does not change until the server responds.

Users may perceive the application as slow or click the action repeatedly.

---

## Optimistic Update

Save the previous state:

```ts
const previousCall = call;
```

Update immediately:

```ts
setCall((current) => ({
  ...current,
  status: "completed",
}));
```

Then execute the server mutation.

If it fails:

```ts
setCall(previousCall);
```

---

## Refactored API Layer

```ts
type CallStatus =
  | "pending"
  | "completed"
  | "cancelled";

async function updateCallStatus(
  callId: number,
  status: CallStatus
): Promise<void> {
  const response = await fetch(
    `/api/calls/${callId}`,
    {
      method: "PATCH",

      headers: {
        "Content-Type":
          "application/json",
      },

      body: JSON.stringify({
        status,
      }),
    }
  );

  if (!response.ok) {
    throw new Error(
      `Failed to update call: ${response.status}`
    );
  }
}
```

---

## Professional Mutation Flow

```tsx
const handleComplete = async () => {
  if (isUpdating) {
    return;
  }

  const previousCall = call;

  setIsUpdating(true);

  setCall((current) => ({
    ...current,
    status: "completed",
  }));

  try {
    await updateCallStatus(
      call.id,
      "completed"
    );
  } catch (error) {
    setCall(previousCall);
  } finally {
    setIsUpdating(false);
  }
};
```

The UI becomes responsive immediately while still tracking whether synchronization is pending.

---

## Why Rollback Matters

Without rollback:

```text
Frontend → Completed
Server   → Pending
```

The client and server disagree.

Optimistic UI requires an error recovery strategy.

Possible strategies include:

- rollback
- refetch
- cache invalidation
- retry
- reconciliation

---

## Updating Items in Lists

For collection state:

```ts
setProperties((current) =>
  current.map((property) =>
    property.id === propertyId
      ? {
          ...property,
          isFavorite:
            !property.isFavorite,
        }
      : property
  )
);
```

This preserves immutability while updating only the target item.

---

## Concurrent Mutations

Optimistic updates become more difficult when multiple mutations happen quickly.

```text
Favorite
Unfavorite
Favorite
```

Requests may finish out of order.

Possible solutions include:

- mutation queues
- request versions
- cancellation
- server-side versioning
- dedicated server-state libraries

Optimistic UI does not eliminate concurrency problems.

---

## Server as Source of Truth

Optimistic state is temporary.

```text
Optimistic State
      ↓
Server Mutation
      ↓
Server Result
      ↓
Reconciliation
```

The server remains the authoritative source for persisted state.

---

## When to Use Optimistic UI

Good candidates include:

- likes
- favorites
- bookmarks
- reactions
- todo completion
- simple status updates

Be more conservative with:

- payments
- money transfers
- account deletion
- permission changes
- irreversible actions

The design should reflect the cost of being wrong.

---

## AI Engineering Connection

Chat interfaces can also use optimistic state.

```ts
interface ChatMessage {
  id: string;

  role:
    | "user"
    | "assistant";

  content: string;

  status:
    | "sending"
    | "sent"
    | "failed";
}
```

When the user submits a prompt:

```ts
const temporaryMessage: ChatMessage = {
  id: crypto.randomUUID(),
  role: "user",
  content: prompt,
  status: "sending",
};

setMessages((current) => [
  ...current,
  temporaryMessage,
]);
```

The message appears immediately.

The application can later mark it as:

```text
sent
```

or:

```text
failed
```

and provide a retry action.

---

## A Better State Model

Instead of thinking only in booleans:

```text
true
false
```

model mutation state explicitly:

```text
Pending
Confirmed
Failed
```

This produces more resilient interfaces.

---

## Exercise

Build an optimistic favorite button.

```ts
interface Property {
  id: number;
  title: string;
  isFavorite: boolean;
}
```

Endpoint:

```text
PATCH /api/properties/:id/favorite
```

Requirements:

1. Update the UI immediately.
2. Save the previous state.
3. Send the API request.
4. Roll back on failure.
5. Prevent accidental duplicate mutations.
6. Display an error when synchronization fails.

### Bonus

Extract the behavior into:

```ts
useOptimisticFavorite()
```

---

## Interview Questions

### What is optimistic UI?

Optimistic UI updates the interface before the server confirms a mutation, assuming the operation will succeed.

If the request fails, the application rolls back or reconciles the optimistic state with the authoritative server state.

### When should optimistic updates be avoided?

They should be used carefully when the cost of displaying an incorrect success state is high, such as payments, permission changes, or irreversible operations.

---

## Key Takeaways

- Optimistic updates improve perceived performance.
- Save enough state to recover from failures.
- Always design rollback or reconciliation.
- Functional state updates help avoid stale state.
- Track pending mutations explicitly.
- Consider concurrent mutations.
- The server remains the source of truth.
- Use optimistic behavior only when the risk is acceptable.

## Daily Engineering Principle

> Make the interface feel instant, but always have a plan for when the server says no.
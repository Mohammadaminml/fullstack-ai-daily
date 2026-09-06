# Day 002 — Preventing Race Conditions with AbortController

## Overview

Fast-changing UI state can create multiple concurrent API requests.

A common example is a search input.

```text
r
re
rea
react
```

Each value may trigger a request.

The problem is that HTTP responses are not guaranteed to arrive in the same order in which they were sent.

This can cause stale data to overwrite newer UI state.

---

## The Problem

```tsx
useEffect(() => {
  async function loadUsers() {
    const response = await fetch(
      `/api/users?search=${search}`
    );

    const data = await response.json();

    setUsers(data);
  }

  loadUsers();
}, [search]);
```

If `search` changes quickly, multiple requests can exist simultaneously.

```text
Request: "react" → 200ms
Request: "re"    → 700ms
```

The older `re` request may finish last and overwrite the correct `react` results.

This is a race condition.

---

## Solution: AbortController

```tsx
useEffect(() => {
  const controller = new AbortController();

  async function loadUsers() {
    try {
      const params = new URLSearchParams({
        search,
      });

      const response = await fetch(
        `/api/users?${params}`,
        {
          signal: controller.signal,
        }
      );

      if (!response.ok) {
        throw new Error(
          `HTTP ${response.status}`
        );
      }

      const data = await response.json();

      setUsers(data);
    } catch (error) {
      if (
        error instanceof DOMException &&
        error.name === "AbortError"
      ) {
        return;
      }

      console.error(error);
    }
  }

  loadUsers();

  return () => {
    controller.abort();
  };
}, [search]);
```

When the dependency changes, React runs the previous effect's cleanup function.

The obsolete request is cancelled before the new request becomes responsible for the UI state.

---

## Request Lifecycle

```text
Search changes
      ↓
Create AbortController
      ↓
Start request
      ↓
Search changes again
      ↓
Effect cleanup
      ↓
Abort old request
      ↓
Start new request
```

---

## Better Architecture

Move request lifecycle logic into a custom hook.

```tsx
function useUserSearch(search: string) {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!search.trim()) {
      setUsers([]);
      return;
    }

    const controller = new AbortController();

    async function searchUsers() {
      try {
        setLoading(true);
        setError(null);

        const params = new URLSearchParams({
          search,
        });

        const response = await fetch(
          `/api/users?${params}`,
          {
            signal: controller.signal,
          }
        );

        if (!response.ok) {
          throw new Error(
            `HTTP ${response.status}`
          );
        }

        const data: User[] =
          await response.json();

        setUsers(data);
      } catch (error) {
        if (
          error instanceof DOMException &&
          error.name === "AbortError"
        ) {
          return;
        }

        setError("Failed to search users");
      } finally {
        if (!controller.signal.aborted) {
          setLoading(false);
        }
      }
    }

    searchUsers();

    return () => controller.abort();
  }, [search]);

  return {
    users,
    loading,
    error,
  };
}
```

The component can now focus on rendering.

---

## Performance Improvement

AbortController can be combined with debouncing.

```text
User Input
    ↓
Debounce
    ↓
API Request
    ↓
AbortController
    ↓
Validation
    ↓
State
    ↓
UI
```

Debouncing reduces how many requests are created.

AbortController cancels requests that are no longer relevant.

They solve related but different problems.

---

## AI Engineering Connection

The same cancellation pattern is useful for long-running AI requests and streaming responses.

```text
Prompt
  ↓
LLM Request
  ↓
AbortSignal
  ↓
Streaming Response
```

Users should be able to cancel obsolete generations without leaving unnecessary work running.

---

## Exercise

Create:

```ts
usePropertySearch()
```

for:

```ts
interface Property {
  id: number;
  title: string;
  price: number;
}
```

Endpoint:

```text
/api/properties?search=apartment
```

Implement:

- loading state
- error state
- empty search handling
- URLSearchParams
- AbortController
- effect cleanup

---

## Interview Question

### How do you prevent stale API responses from updating React state?

Use `AbortController` to cancel obsolete requests inside the `useEffect` cleanup function.

This prevents stale requests from updating the UI and reduces unnecessary network work.

---

## Key Takeaways

- HTTP requests can finish out of order.
- Out-of-order responses can create race conditions.
- `AbortController` can cancel obsolete requests.
- `useEffect` cleanup is a natural place for cancellation.
- Debouncing and cancellation solve different problems.
- Request cancellation is also useful for AI streaming systems.

## Daily Engineering Principle

> If a request is no longer relevant, don't just ignore its result — cancel the work when possible.
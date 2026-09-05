# Day 001 — API Response Validation

## Basic User Interface

```ts
interface User {
  id: number;
  name: string;
  email: string;
  role: string;
}
```

The `User` interface defines the expected structure of a user object.

- `id` must be a number
- `name` must be a string
- `email` must be a string
- `role` must be a string

## Fetching a User

```ts
const getUser = async (): Promise<User> => {
  const response = await fetch("/api/user/42");

  return response.json();
};
```

This function sends a request to:

```text
/api/user/42
```

and expects the result to match the `User` interface.

## Important Note

`Promise<User>` does not validate the API response at runtime.

TypeScript only provides compile-time type safety.

A safer version should validate external data before trusting it.

## Improved Version

```ts
const getUser = async (): Promise<User> => {
  const response = await fetch("/api/user/42");

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }

  const data = await response.json();

  return data;
};
```

## What I Learned

- How TypeScript interfaces work
- How `async/await` works
- What `Promise<User>` means
- How `fetch()` communicates with an API
- Why API responses should not be blindly trusted
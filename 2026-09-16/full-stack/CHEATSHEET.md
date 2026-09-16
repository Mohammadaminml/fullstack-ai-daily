# API Contract Testing Cheatsheet

## اجرای Test

```bash
node --test
node --test --watch
node --test --test-name-pattern="rejects"
```

## Assertionهای پرکاربرد

```js
import assert from "node:assert/strict";

assert.equal(actual, expected);
assert.deepEqual(actual, expected);
assert.throws(() => parse(data), /message/);
await assert.rejects(() => request(), /message/);
```

## بررسی Object خام

```js
function isRecord(value) {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}
```

## بررسی Number

```js
if (typeof value !== "number" || !Number.isFinite(value)) {
  throw new TypeError("Expected a finite number");
}
```

## Fetch Injection

```js
async function load(fetchFn = globalThis.fetch) {
  return fetchFn("/api/resource");
}
```

## سناریوهای ضروری

- Success payload
- Missing required field
- Explicit `null`
- Wrong primitive type
- HTTP `4xx/5xx`
- Invalid input
- Boundary value مثل `0`

## قانون ساده

```text
Network JSON = unknown data
unknown data -> validate -> domain object
```

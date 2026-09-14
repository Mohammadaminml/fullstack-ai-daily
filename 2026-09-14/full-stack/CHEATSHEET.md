# Full-Stack API Error Handling Cheatsheet

## قرارداد پیشنهادی

```ts
type ApiResponse<T> = {
  success: boolean;
  data: T | null;
  error: { code: string; message: string; details?: Record<string, string[]> } | null;
  traceId: string;
};
```

## Status Codeها

| Code | کاربرد |
|---:|---|
| 200 | درخواست موفق |
| 201 | منبع ساخته شد |
| 204 | موفق بدون Body |
| 400 | Validation/ورودی غلط |
| 401 | Authentication لازم است |
| 403 | کاربر احراز شده ولی مجاز نیست |
| 404 | منبع وجود ندارد |
| 409 | تعارض داده |
| 429 | درخواست بیش از حد |
| 500 | خطای داخلی |

## قواعد سریع

- `response.ok` یعنی Status بین 200 تا 299 است.
- خطای Network اصلاً `Response` تولید نمی‌کند و باید با `catch` مدیریت شود.
- `AbortController` برای Timeout یا Cancel کردن Request است.
- `traceId` را در گزارش خطا و Log نگه دارید.
- پیام عمومی به کاربر، جزئیات فنی در Log.
- درخواست `POST` غیر idempotent را کورکورانه Retry نکنید.

## Fetch کوتاه

```ts
const response = await fetch(url, {
  headers: { "Content-Type": "application/json" },
  signal: AbortSignal.timeout(10_000),
});

if (!response.ok) throw new Error(`HTTP ${response.status}`);
const data = await response.json();
```


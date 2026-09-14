# قرارداد API و مدیریت خطای یکپارچه

## هدف

در پایان این آموزش می‌توانید پاسخ موفق و ناموفق API را در ASP.NET Core استاندارد کنید و در React/TypeScript بدون شرط‌های پراکنده مصرف کنید.

## پیش‌نیاز

- آشنایی مقدماتی با C# و ASP.NET Core Minimal API
- آشنایی با TypeScript و `fetch`
- نصب .NET 8 SDK و Node.js 20 یا جدیدتر

## مسئله واقعی

اگر هر Endpoint خطا را با شکل متفاوتی برگرداند، Frontend مجبور می‌شود برای هر Request منطق جداگانه بنویسد. یک قرارداد ساده این مشکل را حل می‌کند:

```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "اطلاعات ورودی معتبر نیست.",
    "details": { "name": ["نام الزامی است."] }
  },
  "traceId": "0HN..."
}
```

## ۱. مدل پاسخ Backend

```csharp
public sealed record ApiError(
    string Code,
    string Message,
    IReadOnlyDictionary<string, string[]>? Details = null);

public sealed record ApiResponse<T>(
    bool Success,
    T? Data,
    ApiError? Error,
    string TraceId);
```

قاعده مهم: برای موفقیت `error` باید `null` و برای شکست `data` باید `null` باشد.

## ۲. انتخاب Status Code درست

| وضعیت | Status |
|---|---:|
| داده نامعتبر | 400 |
| ورود انجام نشده | 401 |
| دسترسی ناکافی | 403 |
| منبع پیدا نشد | 404 |
| تعارض مانند رکورد تکراری | 409 |
| خطای پیش‌بینی‌نشده سرور | 500 |

خطای Business را همیشه با `200` برنگردانید؛ Status Code بخشی از قرارداد HTTP است.

## ۳. Middleware خطای سراسری

Middleware آخرین لایه دفاعی است. خطاهای پیش‌بینی‌نشده را ثبت می‌کند و پاسخ استاندارد می‌سازد، اما جزئیات Exception را در Production افشا نمی‌کند.

```csharp
app.UseExceptionHandler(handler => handler.Run(async context =>
{
    var traceId = context.TraceIdentifier;
    context.Response.StatusCode = StatusCodes.Status500InternalServerError;
    await context.Response.WriteAsJsonAsync(new ApiResponse<object>(
        false,
        null,
        new ApiError("INTERNAL_ERROR", "خطای غیرمنتظره‌ای رخ داد."),
        traceId));
}));
```

## ۴. تعریف Type در Frontend

```ts
export type ApiError = {
  code: string;
  message: string;
  details?: Record<string, string[]>;
};

export type ApiResponse<T> = {
  success: boolean;
  data: T | null;
  error: ApiError | null;
  traceId: string;
};
```

## ۵. Wrapper عمومی برای fetch

Wrapper باید هم خطای HTTP و هم پاسخ JSON نامعتبر یا مشکل Network را مدیریت کند. نمونه کامل در [`examples/api-client.ts`](./examples/api-client.ts) قرار دارد.

```ts
const result = await apiRequest<User>("/api/users/1");

if (!result.ok) {
  console.error(result.error.message, result.error.traceId);
  return;
}

console.log(result.data.name);
```

استفاده از Discriminated Union باعث می‌شود TypeScript بعد از بررسی `ok` نوع داده را دقیق تشخیص دهد.

## اشتباهات رایج

- نمایش مستقیم پیام Exception یا Stack Trace به کاربر
- در نظر گرفتن هر خطا به‌عنوان `500`
- فرض اینکه هر پاسخ خطا حتماً JSON است
- فراموش کردن `encodeURIComponent` برای بخش‌های دینامیک URL
- نمایش پیام فنی به کاربر به جای پیام قابل فهم
- حذف `traceId`؛ این شناسه اتصال گزارش کاربر به Log سرور را آسان می‌کند

## جمع‌بندی

یک قرارداد ثابت، تعداد شرط‌ها و Bugهای Frontend را کم می‌کند. Backend مسئول Status Code، کد خطا و Trace ID است؛ Frontend مسئول نمایش مناسب، Retry منطقی و تجربه کاربری است.


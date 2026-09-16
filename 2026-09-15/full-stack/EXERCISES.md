# تمرین‌های SQL Server Performance

## تمرین 1 — آسان

این شرط را SARGable کن:

```sql
WHERE CONVERT(date, RegisteredDate) = '2026-09-15'
```

راهنمای حل: از بازهٔ `>=` ابتدای روز و `<` ابتدای روز بعد استفاده کن.

## تمرین 2 — متوسط

برای Query زیر Index اولیه پیشنهاد بده:

```sql
SELECT Id, Title, Price
FROM dbo.Properties
WHERE CityId = @CityId AND Price BETWEEN @MinPrice AND @MaxPrice
ORDER BY Price;
```

پاسخ کوتاه:

```sql
CREATE INDEX IX_Properties_CityId_Price
ON dbo.Properties (CityId, Price)
INCLUDE (Title);
```

سپس اثر آن را روی دادهٔ واقعی اندازه بگیر؛ ممکن است طراحی نهایی متفاوت باشد.

## تمرین 3 — چالشی

یک Endpoint صفحه‌بندی‌شده برای تاریخچهٔ تماس داری. Query فعلی بر اساس `UserId` و بازهٔ تاریخ فیلتر و با `CreatedAt DESC` مرتب می‌شود. طراحی کن:

1. Query با ترتیب قطعی
2. Index پوششی اولیه
3. روش مقایسهٔ قبل و بعد

راهنمای حل: `ORDER BY CreatedAt DESC, Id DESC` را برای Tie-breaker در نظر بگیر. با توجه به الگوی Query، Keyهای `(UserId, CreatedAt DESC, Id DESC)` و Columnهای خروجی در `INCLUDE` را آزمایش کن. `STATISTICS IO/TIME` و Actual Plan را ثبت کن.

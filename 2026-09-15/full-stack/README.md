# بهینه‌سازی Query در SQL Server با Index و SARGability

## هدف یادگیری

در پایان می‌توانی Queryهای کند را شناسایی کنی، شرط‌های قابل استفاده توسط Index بنویسی، یک Composite Index منطقی بسازی و اثر آن را با Execution Plan و آمار I/O بسنجی.

## پیش‌نیاز

- آشنایی مقدماتی با `SELECT`، `WHERE` و `ORDER BY`
- SQL Server و یکی از ابزارهای SSMS یا Azure Data Studio
- اجرای نمونه فقط روی دیتابیس آزمایشی

## 1. مسئله چیست؟

وقتی تعداد Rowها زیاد می‌شود، خواندن کل Table یا `Index Scan` می‌تواند پرهزینه باشد. هدف Index این است که SQL Server بتواند محدودهٔ کوچک‌تری را با `Index Seek` پیدا کند. البته `Scan` همیشه بد نیست؛ برای خواندن بخش بزرگی از Table گاهی انتخاب درستی است.

## 2. Query از نوع SARGable

`SARGable` یعنی شرط جست‌وجو به شکلی نوشته شده که موتور دیتابیس بتواند از ساختار مرتب Index استفاده کند.

نمونهٔ نامناسب:

```sql
WHERE CAST(CreatedAt AS date) = '2026-09-15'
```

تابع روی Column قرار گرفته و ممکن است استفادهٔ مؤثر از Index را مختل کند. نسخهٔ بهتر:

```sql
WHERE CreatedAt >= '2026-09-15T00:00:00'
  AND CreatedAt <  '2026-09-16T00:00:00'
```

این الگوی بازهٔ نیمه‌باز، Rowهای همان روز را مستقل از بخش زمان پیدا می‌کند.

## 3. ترتیب Columnها در Composite Index

برای Query زیر:

```sql
SELECT Id, PhoneNumber, Status, CreatedAt
FROM dbo.CallLogs
WHERE UserId = @UserId
  AND CreatedAt >= @From
  AND CreatedAt < @To
ORDER BY CreatedAt DESC;
```

یک انتخاب اولیهٔ مناسب:

```sql
CREATE INDEX IX_CallLogs_UserId_CreatedAt
ON dbo.CallLogs (UserId, CreatedAt DESC)
INCLUDE (PhoneNumber, Status);
```

دلیل طراحی:

- `UserId` شرط Equality است و در ابتدای Key قرار می‌گیرد.
- `CreatedAt` برای Range و Sort استفاده می‌شود.
- `PhoneNumber` و `Status` فقط برای خروجی لازم‌اند؛ `INCLUDE` می‌تواند از Key Lookup جلوگیری کند.

این یک نقطهٔ شروع است، نه قانون همیشگی. Selectivity، حجم داده و Queryهای دیگر باید بررسی شوند.

## 4. اندازه‌گیری قبل و بعد

```sql
SET STATISTICS IO ON;
SET STATISTICS TIME ON;

-- query here

SET STATISTICS TIME OFF;
SET STATISTICS IO OFF;
```

به `logical reads`، زمان CPU، زمان کل و Actual Execution Plan توجه کن. یک اجرای منفرد روی دیتای کم معیار کافی نیست.

## 5. آزمایش عملی

1. فایل [`examples/performance-lab.sql`](./examples/performance-lab.sql) را باز کن.
2. اسکریپت را در محیط آزمایشی اجرا کن.
3. بخش Query نامناسب و مناسب را با Actual Execution Plan مقایسه کن.
4. Index پیشنهادی را ایجاد کن و دوباره `logical reads` را بررسی کن.
5. در پایان Cleanup را اجرا کن.

## نکات مهم

- Index بیشتر به معنی سرعت بیشتر برای همه‌چیز نیست؛ `INSERT`، `UPDATE` و فضای ذخیره‌سازی هزینه دارند.
- نوع Parameter باید با نوع Column یکسان باشد تا Implicit Conversion رخ ندهد.
- در APIها Pagination را قطعی کن؛ `ORDER BY` باید برای Rowهای مساوی یک Tie-breaker مانند `Id` داشته باشد.
- برای تشخیص نهایی، Actual Execution Plan از Estimated Plan مفیدتر است.
- قبل از ساخت Index در Production، Query Store، الگوی مصرف و Indexهای موجود را بررسی کن.

## اشتباهات رایج

- استفاده از `SELECT *` و مجبور کردن دیتابیس به خواندن Columnهای غیرضروری
- قرار دادن `YEAR()`، `LOWER()` یا `CAST()` روی Column فیلترشونده
- ساخت Index جداگانه برای هر Query بدون بررسی هم‌پوشانی
- مقایسهٔ Performance با Cache و دادهٔ آزمایشی غیرواقعی
- تصور اینکه هر `Index Scan` یک خطاست

## ادامه

- [دفترچه تقلب](./CHEATSHEET.md)
- [تمرین‌ها](./EXERCISES.md)
- [نمونهٔ کامل](./examples/performance-lab.sql)

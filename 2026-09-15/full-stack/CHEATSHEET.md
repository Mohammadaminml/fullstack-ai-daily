# SQL Server Performance Cheatsheet

## اندازه‌گیری

```sql
SET STATISTICS IO ON;
SET STATISTICS TIME ON;
-- query
SET STATISTICS TIME OFF;
SET STATISTICS IO OFF;
```

در SSMS برای Actual Execution Plan از `Ctrl+M` استفاده کن.

## الگوهای SARGable

```sql
-- Bad
WHERE YEAR(CreatedAt) = 2026

-- Better
WHERE CreatedAt >= '2026-01-01'
  AND CreatedAt <  '2027-01-01'
```

```sql
-- معمولاً Prefix Search قابلیت استفاده از Index دارد
WHERE PhoneNumber LIKE '0938%'

-- Leading wildcard معمولاً Seek مناسب نمی‌دهد
WHERE PhoneNumber LIKE '%8622'
```

## Composite Index

```sql
CREATE INDEX IX_Table_Equality_Range
ON dbo.TableName (EqualityColumn, RangeColumn DESC)
INCLUDE (OutputColumn1, OutputColumn2);
```

## مشاهدهٔ Indexهای Table

```sql
EXEC sys.sp_helpindex N'dbo.CallLogs';
```

## حذف Index آزمایشی

```sql
DROP INDEX IF EXISTS IX_CallLogs_UserId_CreatedAt
ON dbo.CallLogs;
```

## Checklist

- Columnهای `WHERE` و `JOIN` بررسی شوند.
- Equality پیش از Range ارزیابی شود.
- `INCLUDE` فقط برای پوشش خروجی ضروری استفاده شود.
- نوع Parameter با Column یکسان باشد.
- Logical Reads قبل و بعد ثبت شود.
- هزینهٔ Write و فضای Index فراموش نشود.

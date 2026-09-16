SET NOCOUNT ON;

DROP TABLE IF EXISTS dbo.CallLogsLab;

CREATE TABLE dbo.CallLogsLab
(
    Id bigint IDENTITY(1,1) NOT NULL PRIMARY KEY,
    UserId int NOT NULL,
    PhoneNumber varchar(20) NOT NULL,
    Status tinyint NOT NULL,
    CreatedAt datetime2(0) NOT NULL
);

;WITH Numbers AS
(
    SELECT TOP (20000)
        ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS n
    FROM sys.all_objects AS a
    CROSS JOIN sys.all_objects AS b
)
INSERT dbo.CallLogsLab (UserId, PhoneNumber, Status, CreatedAt)
SELECT
    1 + (n % 200),
    CONCAT('09', RIGHT(CONCAT('000000000', n), 9)),
    n % 4,
    DATEADD(minute, n, CAST('2026-09-01' AS datetime2(0)))
FROM Numbers;

SET STATISTICS IO ON;
SET STATISTICS TIME ON;

-- Non-SARGable: تابع روی Column
SELECT Id, PhoneNumber, Status, CreatedAt
FROM dbo.CallLogsLab
WHERE UserId = 42
  AND CAST(CreatedAt AS date) = '2026-09-10';

-- SARGable: بازه نیمه‌باز
SELECT Id, PhoneNumber, Status, CreatedAt
FROM dbo.CallLogsLab
WHERE UserId = 42
  AND CreatedAt >= '2026-09-10T00:00:00'
  AND CreatedAt <  '2026-09-11T00:00:00'
ORDER BY CreatedAt DESC;

CREATE INDEX IX_CallLogsLab_UserId_CreatedAt
ON dbo.CallLogsLab (UserId, CreatedAt DESC)
INCLUDE (PhoneNumber, Status);

-- Query را پس از ساخت Index دوباره اجرا و Plan/IO را مقایسه کن
SELECT Id, PhoneNumber, Status, CreatedAt
FROM dbo.CallLogsLab
WHERE UserId = 42
  AND CreatedAt >= '2026-09-10T00:00:00'
  AND CreatedAt <  '2026-09-11T00:00:00'
ORDER BY CreatedAt DESC;

SET STATISTICS TIME OFF;
SET STATISTICS IO OFF;

-- Cleanup اختیاری
-- DROP TABLE dbo.CallLogsLab;

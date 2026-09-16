# دفترچه روزانه Full‑Stack و AI — 2026-09-15

بستهٔ امروز دو مهارت مکمل را پوشش می‌دهد: سریع‌تر کردن Queryهای SQL Server و ساخت هستهٔ Retrieval برای یک سامانهٔ RAG.

## فهرست مطالب

| مسیر | موضوع | زمان پیشنهادی |
| --- | --- | --- |
| [Full‑Stack](./full-stack/README.md) | Index و Queryهای `SARGable` در SQL Server | 60–75 دقیقه |
| [AI](./ai/README.md) | Chunking، Retrieval و Citation در RAG | 60–90 دقیقه |

## مسیر پیشنهادی مطالعه

1. آموزش Full‑Stack را بخوان و اسکریپت `performance-lab.sql` را در یک دیتابیس آزمایشی اجرا کن.
2. `CHEATSHEET.md` همان بخش را برای مرور سریع ذخیره کن.
3. آموزش AI را بخوان و نمونهٔ Python را اجرا کن.
4. خروجی Retrieval را بررسی و سپس تمرین‌های هر دو بخش را حل کن.

> تمام اسکریپت‌های دیتابیس را ابتدا در محیط Development اجرا کن، نه Production.

## اجرای سریع

```bash
cd 2026-09-15/ai/examples
python3 rag_retriever.py
```

برای SQL Server، فایل [`performance-lab.sql`](./full-stack/examples/performance-lab.sql) را با SSMS یا Azure Data Studio اجرا کن.

## انتشار

دستورهای آماده در [publish-guide.md](./publish-guide.md) قرار دارند.

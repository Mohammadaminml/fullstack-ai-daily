# ارزیابی RAG با Recall@k، MRR و Citation Validation

## هدف یادگیری

در پایان می‌توانی یک Dataset کوچک ارزیابی بسازی، کیفیت Retrieval را با `Recall@k` و `MRR` بسنجی، Citationهای پاسخ را Validate کنی و Regression را پیش از انتشار تشخیص بدهی.

## پیش‌نیاز

- Python 3.10 یا جدیدتر
- آشنایی با مراحل `Chunking` و `Retrieval`
- شناخت مقدماتی RAG

نمونه فقط از Python Standard Library استفاده می‌کند.

## 1. چرا Evaluation لازم است؟

دیدن چند پاسخ خوب کافی نیست. تغییر `chunk_size`، مدل Embedding، `top_k` یا فیلتر Metadata می‌تواند بعضی سؤال‌ها را بهتر و بعضی را بدتر کند. Dataset ثابت و Metric قابل تکرار، این تغییر را قابل مشاهده می‌کند.

## 2. Dataset ارزیابی

هر Case حداقل شامل این موارد است:

```json
{
  "query": "تاریخچه تماس چه اطلاعاتی دارد؟",
  "relevant_source_ids": ["call-logging"]
}
```

برای پروژهٔ واقعی بهتر است Caseها از سؤال‌های واقعی کاربران، با حذف دادهٔ حساس، تهیه و توسط فرد آشنا با Domain برچسب‌گذاری شوند.

## 3. Recall@k

این Metric بررسی می‌کند چه سهمی از منابع مرتبط در میان `k` نتیجهٔ اول بازیابی شده‌اند:

```text
Recall@k = retrieved relevant sources / all relevant sources
```

اگر دو منبع مرتبط وجود داشته باشد و فقط یکی در سه نتیجهٔ اول باشد، `Recall@3 = 0.5` است.

## 4. Mean Reciprocal Rank

`Reciprocal Rank` به رتبهٔ اولین نتیجهٔ مرتبط حساس است:

```text
RR = 1 / rank_of_first_relevant_result
```

اگر اولین منبع مرتبط رتبهٔ دوم باشد، `RR = 0.5`. میانگین این مقدار روی همهٔ Caseها، `MRR` است.

## 5. Citation Validation

اگر مدل `[source=permissions]` تولید کند، حداقل باید بررسی کنیم:

1. Citation از نظر Syntax معتبر است.
2. `source_id` در Context بازیابی‌شده وجود دارد.
3. برای ارزیابی قوی‌تر، متن منبع واقعاً ادعای مجاور Citation را پشتیبانی می‌کند.

نمونهٔ امروز دو مورد اول را قطعی بررسی می‌کند. مورد سوم به Dataset ادعا–شاهد یا ارزیابی انسانی/مدلی دقیق‌تر نیاز دارد.

## 6. اجرای Evaluation Harness

```bash
cd 2026-09-16/ai/examples
python3 evaluate_rag.py
```

خروجی شامل نتیجهٔ هر Case، Metricهای کل و نتیجهٔ Citation Validation است. اگر Thresholdها پاس نشوند، Process با Exit Code غیرصفر تمام می‌شود و می‌توان آن را در CI استفاده کرد.

## 7. استفاده در CI

یک Gate ساده:

```text
mean Recall@3 >= 0.80
MRR >= 0.75
invalid citation count == 0
```

Thresholdها باید از Baseline واقعی پروژه گرفته شوند. عددهای بالا فقط نمونه‌اند و استاندارد عمومی نیستند.

## نکات مهم

- Dataset ارزیابی را از Dataset توسعه جدا نگه دار.
- Metric بازیابی خوب، کیفیت پاسخ نهایی را تضمین نمی‌کند.
- سؤال‌های بدون پاسخ را هم Test کن تا سیستم مجبور به حدس نشود.
- Evaluation را بر اساس زبان، نوع سند و گروه کاربری تفکیک کن.
- تغییرات Dataset و Labelها را Version Control کن.
- دادهٔ حساس را وارد Log یا Repository عمومی نکن.

## اشتباهات رایج

- ارزیابی روی همان سؤال‌هایی که برای تنظیم سیستم استفاده شده‌اند
- گزارش فقط میانگین و پنهان کردن Caseهای شکست‌خورده
- معتبر دانستن هر Citation صرفاً به‌خاطر وجود Source ID
- تغییر هم‌زمان چند پارامتر و نامشخص شدن علت تغییر Metric
- نادیده گرفتن سؤال‌های بدون پاسخ یا اسناد دارای Prompt Injection

## ادامه

- [دفترچه تقلب](./CHEATSHEET.md)
- [تمرین‌ها](./EXERCISES.md)
- [Evaluation Harness](./examples/evaluate_rag.py)

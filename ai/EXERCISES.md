# تمرین‌های AI

## ۱. آسان — محاسبه Cosine

تابعی بنویسید که Cosine Similarity بردارهای `[1, 0, 1]` و `[1, 1, 0]` را محاسبه کند.

پاسخ کنترل: مقدار تقریبی `0.5` است.

## ۲. متوسط — Metadata Filter

به `Document` فیلد `category` اضافه کنید و تابع `search` را طوری تغییر دهید که فقط در Category انتخاب‌شده جست‌وجو کند.

راهنما: Filter را قبل از محاسبه شباهت اجرا کنید تا محاسبات اضافه انجام نشود.

## ۳. چالشی — ارزیابی Recall@K

مجموعه‌ای شامل Query و شناسه سند مرتبط بسازید. تابعی بنویسید که بررسی کند سند درست بین K نتیجه اول وجود دارد یا نه و میانگین Recall@K را گزارش دهد.

راهنمای حل:

```python
hits = sum(expected_id in returned_ids[:k] for query, expected_id in test_set)
recall_at_k = hits / len(test_set)
```

سپس اثر مقادیر مختلف `DIMENSIONS` و `top_k` را مقایسه کنید.


# Embedding & Semantic Search Cheatsheet

## واژه‌ها

| اصطلاح | معنی کوتاه |
|---|---|
| Embedding | نمایش برداری داده |
| Dimension | تعداد مؤلفه‌های بردار |
| Cosine Similarity | شباهت جهت دو بردار |
| Top-K | تعداد نتایج برتر |
| Chunk | قطعه‌ای از سند |
| Vector Store | محل ذخیره و جست‌وجوی بردارها |
| Metadata Filter | محدودسازی نتایج بر اساس ویژگی‌ها |

## فرمول‌ها

```text
dot(A, B) = Σ(A[i] × B[i])
norm(A)   = √Σ(A[i]²)
cosine    = dot(A, B) / (norm(A) × norm(B))
```

## چک‌لیست RAG

- [ ] اسناد پاک و نسخه‌بندی شده‌اند.
- [ ] Chunkها Metadata دارند.
- [ ] مدل Query و Document یکسان است.
- [ ] Filter سطح دسترسی اجرا می‌شود.
- [ ] Top-K و Threshold با داده واقعی تنظیم شده‌اند.
- [ ] Citation به منبع اصلی نگه داشته می‌شود.
- [ ] Retrieval با معیارهایی مانند Recall@K ارزیابی می‌شود.

## انتخاب‌های اولیه پیشنهادی برای آزمایش

```text
chunk size: 300–800 tokens
overlap:    10–20%
top-k:      3–8
```

این اعداد قانون ثابت نیستند؛ با داده و معیار ارزیابی تنظیمشان کنید.


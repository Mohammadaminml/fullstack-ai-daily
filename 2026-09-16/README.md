# دفترچه روزانه Full‑Stack و AI — 2026-09-16

بستهٔ امروز دربارهٔ اعتمادپذیری است: در Full‑Stack قرارداد API را با Test محافظت می‌کنیم و در AI کیفیت Retrieval و Citation را اندازه می‌گیریم.

## فهرست مطالب

| مسیر | موضوع | زمان پیشنهادی |
| --- | --- | --- |
| [Full‑Stack](./full-stack/README.md) | Contract Testing برای API Client | 60–75 دقیقه |
| [AI](./ai/README.md) | ارزیابی RAG با Recall@k، MRR و Citation Validation | 75–90 دقیقه |

## مسیر پیشنهادی مطالعه

1. آموزش Full‑Stack را بخوان و Testهای نمونه را اجرا کن.
2. عمداً شکل Payload را تغییر بده و شکست Test را مشاهده کن.
3. آموزش AI را بخوان و Evaluation Harness را اجرا کن.
4. یک Case جدید به Dataset ارزیابی اضافه کن و اثر آن را روی Metricها ببین.
5. تمرین‌های دو بخش را از آسان به چالشی حل کن.

## اجرای سریع

```bash
cd 2026-09-16/full-stack/examples
npm test

cd ../../ai/examples
python3 evaluate_rag.py
```

## انتشار

دستورهای دقیق Commit و Push در [publish-guide.md](./publish-guide.md) قرار دارند.

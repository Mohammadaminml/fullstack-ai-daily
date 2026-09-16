# RAG Evaluation Cheatsheet

## Dataset Case

```python
{
    "query": "...",
    "relevant_source_ids": {"source-a", "source-b"},
}
```

## Recall@k

```python
retrieved = set(result_ids[:k])
recall = len(retrieved & relevant) / len(relevant)
```

## Reciprocal Rank

```python
rr = next(
    (1 / rank for rank, source_id in enumerate(result_ids, 1) if source_id in relevant),
    0.0,
)
```

## Citation Pattern

```python
import re

citations = re.findall(r"\[source=([\w-]+)\]", answer)
```

## Minimum Evaluation Set

- سؤال ساده با یک منبع مرتبط
- سؤال چندمنبعی
- سؤال دارای واژه‌های مشابه اما معنای متفاوت
- سؤال بدون پاسخ
- سؤال فارسی با شکل‌های مختلف `ی/ي` و `ک/ك`
- سند غیرمجاز برای کاربر

## CI Gate

```python
if recall_at_3 < baseline or invalid_citations:
    raise SystemExit(1)
```

## تفکیک Metricها

- Retrieval: `Recall@k`, `MRR`, `nDCG`
- Generation: groundedness، completeness، refusal quality
- Citation: validity، correctness، completeness
- Operations: latency، error rate، token/cost usage

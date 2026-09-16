"""Small deterministic evaluation harness for educational RAG experiments."""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Document:
    source_id: str
    text: str


@dataclass(frozen=True)
class EvalCase:
    query: str
    relevant_source_ids: frozenset[str]


def tokenize(text: str) -> set[str]:
    normalized = text.replace("ي", "ی").replace("ك", "ک").lower()
    return set(re.findall(r"[\w\u0600-\u06ff]+", normalized, flags=re.UNICODE))


def retrieve(query: str, documents: list[Document], top_k: int = 3) -> list[str]:
    query_tokens = tokenize(query)
    scored: list[tuple[float, str]] = []
    for document in documents:
        document_tokens = tokenize(document.text)
        score = len(query_tokens & document_tokens) / max(len(query_tokens), 1)
        if score > 0:
            scored.append((score, document.source_id))
    scored.sort(key=lambda item: (-item[0], item[1]))
    return [source_id for _, source_id in scored[:top_k]]


def recall_at_k(result_ids: list[str], relevant_ids: frozenset[str], k: int) -> float:
    if not relevant_ids:
        raise ValueError("relevant_ids must not be empty")
    retrieved = set(result_ids[:k])
    return len(retrieved & relevant_ids) / len(relevant_ids)


def reciprocal_rank(result_ids: list[str], relevant_ids: frozenset[str]) -> float:
    for rank, source_id in enumerate(result_ids, start=1):
        if source_id in relevant_ids:
            return 1.0 / rank
    return 0.0


def extract_citations(answer: str) -> list[str]:
    return re.findall(r"\[source=([\w-]+)\]", answer)


def invalid_citations(answer: str, context_source_ids: set[str]) -> list[str]:
    return sorted(set(extract_citations(answer)) - context_source_ids)


def run_evaluation(documents: list[Document], cases: list[EvalCase], k: int = 3) -> tuple[float, float]:
    recalls: list[float] = []
    reciprocal_ranks: list[float] = []

    for index, case in enumerate(cases, start=1):
        result_ids = retrieve(case.query, documents, top_k=k)
        recall = recall_at_k(result_ids, case.relevant_source_ids, k)
        rr = reciprocal_rank(result_ids, case.relevant_source_ids)
        recalls.append(recall)
        reciprocal_ranks.append(rr)
        print(f"case={index} recall@{k}={recall:.3f} rr={rr:.3f} results={result_ids}")

    return sum(recalls) / len(recalls), sum(reciprocal_ranks) / len(reciprocal_ranks)


def main() -> None:
    documents = [
        Document("call-logging", "تاریخچه تماس شامل شناسه کاربر، کارشناس، نتیجه تماس و زمان پیگیری است."),
        Document("permissions", "سطح دسترسی باید پیش از بازیابی تاریخچه تماس بررسی شود تا داده محرمانه نشت نکند."),
        Document("phone-search", "شماره تلفن قبل از جست‌وجوی پروفایل Normalize می‌شود."),
        Document("property-price", "قیمت ملک بر حسب ریال ذخیره و به صورت عدد نمایش داده می‌شود."),
    ]
    cases = [
        EvalCase("تاریخچه تماس چه اطلاعاتی دارد؟", frozenset({"call-logging"})),
        EvalCase("چطور جلوی نشت تاریخچه محرمانه را بگیریم؟", frozenset({"permissions"})),
        EvalCase("شماره تلفن پیش از جستجو چه می‌شود؟", frozenset({"phone-search"})),
    ]

    mean_recall, mrr = run_evaluation(documents, cases, k=3)
    print(f"\nmean_recall@3={mean_recall:.3f}")
    print(f"mrr={mrr:.3f}")

    retrieved_context = {"call-logging", "permissions"}
    good_answer = "ثبت تماس شامل نتیجه و زمان پیگیری است. [source=call-logging]"
    bad_answer = "قیمت نیز ثبت می‌شود. [source=made-up-source]"
    assert invalid_citations(good_answer, retrieved_context) == []
    assert invalid_citations(bad_answer, retrieved_context) == ["made-up-source"]
    print("citation_validation=passed")

    minimum_recall = 0.80
    minimum_mrr = 0.75
    if mean_recall < minimum_recall or mrr < minimum_mrr:
        raise SystemExit("Evaluation gate failed")


if __name__ == "__main__":
    main()

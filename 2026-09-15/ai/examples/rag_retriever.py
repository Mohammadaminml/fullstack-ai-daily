"""Educational RAG retriever using only Python's standard library."""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class Chunk:
    source_id: str
    chunk_id: int
    text: str


@dataclass(frozen=True)
class SearchResult:
    chunk: Chunk
    score: float


def tokenize(text: str) -> set[str]:
    normalized = text.replace("ي", "ی").replace("ك", "ک").lower()
    return set(re.findall(r"[\w\u0600-\u06ff]+", normalized, flags=re.UNICODE))


def chunk_text(text: str, chunk_size: int = 35, overlap: int = 8) -> list[str]:
    if chunk_size <= 0 or not 0 <= overlap < chunk_size:
        raise ValueError("Require chunk_size > 0 and 0 <= overlap < chunk_size")

    words = text.split()
    step = chunk_size - overlap
    return [" ".join(words[i : i + chunk_size]) for i in range(0, len(words), step)]


def build_chunks(documents: dict[str, str]) -> list[Chunk]:
    chunks: list[Chunk] = []
    for source_id, text in documents.items():
        for chunk_id, content in enumerate(chunk_text(text)):
            chunks.append(Chunk(source_id, chunk_id, content))
    return chunks


def retrieve(query: str, chunks: list[Chunk], top_k: int = 3) -> list[SearchResult]:
    if top_k <= 0:
        return []

    query_tokens = tokenize(query)
    if not query_tokens:
        return []

    results: list[SearchResult] = []
    for chunk in chunks:
        overlap = query_tokens & tokenize(chunk.text)
        score = len(overlap) / len(query_tokens)
        if score > 0:
            results.append(SearchResult(chunk, score))

    return sorted(
        results,
        key=lambda item: (-item.score, item.chunk.source_id, item.chunk.chunk_id),
    )[:top_k]


def build_context(results: list[SearchResult]) -> str:
    return "\n\n".join(
        f"[source={item.chunk.source_id} chunk={item.chunk.chunk_id}]\n{item.chunk.text}"
        for item in results
    )


def main() -> None:
    documents = {
        "call-logging": (
            "برای ثبت تماس ابتدا شماره تلفن در CRM جست‌وجو می‌شود. اگر پروفایل کاربر وجود داشته باشد، "
            "کارشناس نتیجه تماس، توضیحات و زمان پیگیری بعدی را ثبت می‌کند. هر رکورد تاریخچه تماس باید "
            "شناسه کاربر، شناسه کارشناس و زمان ایجاد داشته باشد."
        ),
        "permissions": (
            "نمایش تاریخچه تماس تابع سطح دسترسی کاربر است. فیلتر مجوز باید پیش از بازیابی اطلاعات اعمال شود "
            "تا داده محرمانه وارد Context مدل نشود. ثبت رویداد دسترسی برای بررسی امنیتی ضروری است."
        ),
        "search": (
            "شماره تلفن پیش از جست‌وجو Normalize می‌شود. فاصله، خط تیره و پیش‌شماره‌های معادل باید به شکل "
            "یکسان تبدیل شوند تا پروفایل تکراری ساخته نشود."
        ),
    }

    query = " ".join(sys.argv[1:]) or "تاریخچه تماس چه اطلاعاتی باید ثبت کند؟"
    chunks = build_chunks(documents)
    results = retrieve(query, chunks)

    print(f"Query: {query}")
    print(f"Retrieved: {len(results)} chunk(s)\n")
    for item in results:
        print(
            f"score={item.score:.3f} source={item.chunk.source_id} "
            f"chunk={item.chunk.chunk_id}"
        )

    print("\nContext for the LLM:\n")
    print(build_context(results) or "No relevant context found.")


if __name__ == "__main__":
    main()

"""A dependency-free educational semantic-search pipeline.

This hashing vectorizer demonstrates vectorization and ranking. It is not a
replacement for a trained multilingual embedding model.
"""

from __future__ import annotations

import hashlib
import math
import re
import sys
from dataclasses import dataclass


DIMENSIONS = 128


@dataclass(frozen=True)
class Document:
    id: int
    title: str
    text: str


def tokenize(text: str) -> list[str]:
    return re.findall(r"[\w\u0600-\u06FF]+", text.lower(), flags=re.UNICODE)


def embed(text: str, dimensions: int = DIMENSIONS) -> list[float]:
    vector = [0.0] * dimensions
    for token in tokenize(text):
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        index = int.from_bytes(digest[:4], "big") % dimensions
        sign = 1.0 if digest[4] % 2 == 0 else -1.0
        vector[index] += sign

    magnitude = math.sqrt(sum(value * value for value in vector))
    return [value / magnitude for value in vector] if magnitude else vector


def cosine_similarity(left: list[float], right: list[float]) -> float:
    if len(left) != len(right):
        raise ValueError("Vectors must have equal dimensions")
    return sum(a * b for a, b in zip(left, right))


def search(query: str, documents: list[Document], top_k: int = 3):
    query_vector = embed(query)
    ranked = []
    for document in documents:
        document_vector = embed(f"{document.title} {document.text}")
        score = cosine_similarity(query_vector, document_vector)
        ranked.append((score, document))
    return sorted(ranked, key=lambda item: item[0], reverse=True)[:top_k]


def main() -> None:
    documents = [
        Document(1, "مدیریت خطای API", "React TypeScript fetch network error timeout"),
        Document(2, "احراز هویت", "ASP.NET Core JWT login refresh token authorization"),
        Document(3, "پایگاه داده", "SQL Server index query performance execution plan"),
        Document(4, "هوش مصنوعی", "RAG embedding vector database semantic retrieval"),
    ]
    query = " ".join(sys.argv[1:]) or "react api error"
    print(f"Query: {query}\n")
    for score, document in search(query, documents):
        print(f"{score: .4f} | {document.id} | {document.title}")


if __name__ == "__main__":
    main()


from __future__ import annotations

import hashlib
import math
import re
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Document:
    document_id: str
    tenant_id: str
    title: str
    body: str
    allowed_users: frozenset[str]


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    document_id: str
    tenant_id: str
    title: str
    text: str
    allowed_users: frozenset[str]


@dataclass(frozen=True)
class SearchHit:
    chunk: Chunk
    score: float


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z0-9_]+", text.lower())


def chunk_document(document: Document, max_words: int = 48, overlap: int = 8) -> list[Chunk]:
    words = document.body.split()
    chunks: list[Chunk] = []
    step = max(1, max_words - overlap)

    for index, start in enumerate(range(0, len(words), step)):
        window = words[start : start + max_words]
        if not window:
            continue
        text = " ".join(window)
        chunk_id = f"{document.document_id}:{index}"
        chunks.append(
            Chunk(
                chunk_id=chunk_id,
                document_id=document.document_id,
                tenant_id=document.tenant_id,
                title=document.title,
                text=text,
                allowed_users=document.allowed_users,
            )
        )
    return chunks


class HashEmbedder:
    """Dependency-free toy embedder. Replace with a real embedding model in production."""

    def __init__(self, dimensions: int = 64) -> None:
        self.dimensions = dimensions

    def embed(self, text: str) -> list[float]:
        vector = [0.0] * self.dimensions
        for token in tokenize(text):
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            bucket = int.from_bytes(digest[:4], "big") % self.dimensions
            sign = 1.0 if digest[4] % 2 == 0 else -1.0
            vector[bucket] += sign
        return normalize(vector)


def normalize(vector: list[float]) -> list[float]:
    norm = math.sqrt(sum(value * value for value in vector))
    if norm == 0:
        return vector
    return [value / norm for value in vector]


def cosine(a: list[float], b: list[float]) -> float:
    return sum(left * right for left, right in zip(a, b))


class InMemoryVectorStore:
    def __init__(self, embedder: HashEmbedder) -> None:
        self.embedder = embedder
        self.rows: list[tuple[Chunk, list[float]]] = []

    def upsert_chunks(self, chunks: Iterable[Chunk]) -> None:
        for chunk in chunks:
            self.rows = [(existing, vector) for existing, vector in self.rows if existing.chunk_id != chunk.chunk_id]
            self.rows.append((chunk, self.embedder.embed(chunk.text)))

    def delete_document(self, document_id: str) -> None:
        self.rows = [(chunk, vector) for chunk, vector in self.rows if chunk.document_id != document_id]

    def search(
        self,
        query: str,
        *,
        tenant_id: str,
        user_id: str,
        top_k: int = 8,
    ) -> list[SearchHit]:
        query_vector = self.embedder.embed(query)
        hits: list[SearchHit] = []

        for chunk, vector in self.rows:
            if chunk.tenant_id != tenant_id:
                continue
            if user_id not in chunk.allowed_users:
                continue
            hits.append(SearchHit(chunk=chunk, score=cosine(query_vector, vector)))

        return sorted(hits, key=lambda hit: hit.score, reverse=True)[:top_k]


def token_overlap_rerank(query: str, hits: list[SearchHit], top_k: int = 4) -> list[SearchHit]:
    query_tokens = set(tokenize(query))

    def rerank_score(hit: SearchHit) -> float:
        chunk_tokens = set(tokenize(hit.chunk.text + " " + hit.chunk.title))
        overlap = len(query_tokens & chunk_tokens)
        return hit.score + 0.08 * overlap

    return sorted(hits, key=rerank_score, reverse=True)[:top_k]


def generate_answer(query: str, hits: list[SearchHit]) -> str:
    if not hits:
        return "関連する根拠が見つかりませんでした。"

    citations = ", ".join(f"{hit.chunk.title}#{hit.chunk.chunk_id}" for hit in hits)
    context = "\n".join(f"- {hit.chunk.text}" for hit in hits)
    return (
        f"質問: {query}\n\n"
        "回答案: 検索された根拠に基づくと、以下の情報が関連します。\n"
        f"{context}\n\n"
        f"引用: {citations}"
    )


def evaluate_recall_at_k(
    store: InMemoryVectorStore,
    eval_cases: list[tuple[str, str]],
    *,
    tenant_id: str,
    user_id: str,
    k: int,
) -> float:
    if not eval_cases:
        return 0.0

    hits = 0
    for query, expected_document_id in eval_cases:
        results = store.search(query, tenant_id=tenant_id, user_id=user_id, top_k=k)
        returned_document_ids = {hit.chunk.document_id for hit in results}
        if expected_document_id in returned_document_ids:
            hits += 1
    return hits / len(eval_cases)


def main() -> None:
    documents = [
        Document(
            document_id="doc_pgvector",
            tenant_id="tenant_a",
            title="pgvector運用メモ",
            body="PostgreSQL と pgvector は小中規模 RAG で有効です。権限やメタデータを SQL で扱えるため既存システムに統合しやすいです。",
            allowed_users=frozenset({"alice"}),
        ),
        Document(
            document_id="doc_hnsw",
            tenant_id="tenant_a",
            title="HNSWの特徴",
            body="HNSW は近傍グラフをたどって高速に検索します。高い recall を出しやすい一方でメモリ消費と構築時間に注意が必要です。",
            allowed_users=frozenset({"alice", "bob"}),
        ),
        Document(
            document_id="doc_secret",
            tenant_id="tenant_b",
            title="別テナントの秘密文書",
            body="この文書は tenant_b のデータなので tenant_a のユーザーには検索結果として出してはいけません。",
            allowed_users=frozenset({"mallory"}),
        ),
    ]

    embedder = HashEmbedder(dimensions=64)
    store = InMemoryVectorStore(embedder)

    for document in documents:
        store.upsert_chunks(chunk_document(document))

    query = "小中規模RAGでPostgreSQLを使う利点は？"
    first_pass = store.search(query, tenant_id="tenant_a", user_id="alice", top_k=8)
    reranked = token_overlap_rerank(query, first_pass, top_k=3)
    print(generate_answer(query, reranked))

    eval_cases = [
        ("pgvector はどんな場合に向く？", "doc_pgvector"),
        ("HNSW はなぜ速い？", "doc_hnsw"),
    ]
    recall = evaluate_recall_at_k(store, eval_cases, tenant_id="tenant_a", user_id="alice", k=3)
    print(f"\nrecall@3={recall:.2f}")


if __name__ == "__main__":
    main()

# Day 006 — Building RAG with Embeddings and Vector Search

## Overview

Retrieval-Augmented Generation (RAG) allows LLM applications to use external knowledge without placing the entire knowledge base into every prompt.

A typical RAG pipeline looks like:

```text
Question
   ↓
Embedding
   ↓
Retrieval
   ↓
Relevant Context
   ↓
LLM
   ↓
Answer
```

---

## Why RAG?

A naive application might send every document to the model:

```ts
const prompt = `
Documentation:

${allDocuments}

Question:

${question}
`;

const answer =
  await generateAnswer(prompt);
```

As the knowledge base grows, this creates problems with:

- token usage
- latency
- cost
- context limits
- irrelevant information

Instead, retrieve only the information relevant to the current question.

---

## Embeddings

An embedding converts content into a numerical vector.

Conceptually:

```text
"React builds user interfaces"

↓

[0.21, -0.44, 0.91, ...]
```

Semantically similar content tends to have nearby vector representations.

This enables semantic search.

---

## Retrieval

Create an embedding for the user's question:

```ts
const queryVector =
  await createEmbedding(question);
```

Search the vector store:

```ts
const documents =
  await vectorStore.search({
    vector: queryVector,
    limit: 5,
  });
```

Build context:

```ts
const context = documents
  .map(
    document => document.content
  )
  .join("\n\n");
```

Generate an answer:

```ts
const answer =
  await generateAnswer(`
    Answer using only the context.

    If the context does not contain
    enough information, say so.

    Context:
    ${context}

    Question:
    ${question}
  `);
```

---

## Separate Retrieval and Generation

```ts
class DocumentRetriever {
  constructor(
    private readonly vectorStore:
      VectorStore
  ) {}

  async retrieve(
    question: string
  ) {
    const vector =
      await createEmbedding(question);

    return this.vectorStore.search(
      vector,
      5
    );
  }
}
```

Then:

```ts
class RAGService {
  constructor(
    private readonly retriever:
      DocumentRetriever
  ) {}

  async answer(
    question: string
  ) {
    const documents =
      await this.retriever.retrieve(
        question
      );

    const context = documents
      .map(doc => doc.content)
      .join("\n\n");

    return generateAnswer(`
      Answer using only this context:

      ${context}

      Question:
      ${question}
    `);
  }
}
```

This separation makes retrieval easier to test and evaluate independently.

---

## Document Ingestion

Documents are normally processed before users search them.

```text
Documents
   ↓
Chunking
   ↓
Embeddings
   ↓
Vector Storage
```

Conceptually:

```ts
const chunks =
  splitDocument(document);

const embeddings =
  await createEmbeddings(
    chunks.map(
      chunk => chunk.content
    )
  );
```

Batching embeddings can reduce unnecessary remote calls.

---

## Chunking

Chunk size affects retrieval quality.

```text
Chunks too large
→ less precise retrieval

Chunks too small
→ insufficient context
```

Chunk size and overlap should be evaluated against the actual dataset rather than chosen blindly.

---

## Metadata Filtering

Vector similarity can be combined with structured filters.

Example metadata:

```ts
{
  cityId: 1,
  category: "agency"
}
```

Search:

```ts
vectorStore.search({
  vector,
  limit: 5,

  filter: {
    cityId: 1,
  },
});
```

This combines semantic retrieval with deterministic constraints.

---

## RAG Is More Than Vector Search

RAG is an architecture pattern.

Retrieval can use:

- vector search
- keyword search
- SQL
- APIs
- metadata filtering
- search engines
- hybrid search

The correct retriever depends on the data and the user's question.

---

## Evaluation

Do not evaluate only the final LLM answer.

Evaluate retrieval independently.

Example dataset:

```ts
const evaluationSet = [
  {
    question:
      "How do I register an agency?",

    expectedDocumentId:
      "agency-registration",
  },
];
```

Useful retrieval metrics include:

- Recall@K
- Precision@K
- Mean Reciprocal Rank

For example, Recall@5 asks whether the relevant document appeared within the top five retrieved results.

---

## Debugging RAG

Inspect the complete pipeline:

```text
Question
 ↓
Query Embedding
 ↓
Retrieved Documents
 ↓
Scores
 ↓
Metadata
 ↓
Context
 ↓
Prompt
 ↓
Answer
```

A fundamental rule is:

```text
Bad Retrieval
     ↓
Bad Context
     ↓
Bad Answer
```

Prompt engineering cannot reliably compensate for missing knowledge.

---

## Exercise

Build a simple RAG pipeline for CRM documentation.

Documents:

```ts
const documents = [
  {
    id: "agency-registration",
    content:
      "Agencies must provide...",
  },

  {
    id: "customer-calls",
    content:
      "Customer call history...",
  },

  {
    id: "password-reset",
    content:
      "Users can reset...",
  },
];
```

Implement:

```text
Documents
 ↓
Chunking
 ↓
Embedding
 ↓
Vector Store
```

Then:

```text
Question
 ↓
Embedding
 ↓
Top-3 Retrieval
 ↓
Context
 ↓
LLM
```

### Bonus

Add metadata:

```ts
interface Metadata {
  category:
    | "agency"
    | "customer"
    | "authentication";
}
```

and support metadata-filtered retrieval.

---

## Interview Questions

### What is RAG?

Retrieval-Augmented Generation retrieves relevant external knowledge before generation and provides that context to an LLM.

### What are embeddings?

Embeddings are numerical vector representations that capture semantic properties of data and enable similarity-based retrieval.

### Why evaluate retrieval separately?

Because poor retrieval produces poor context, and an LLM cannot reliably answer questions when the required knowledge was never retrieved.

---

## Key Takeaways

- RAG connects LLMs to external knowledge.
- Embeddings enable semantic retrieval.
- Retrieve relevant context instead of sending everything.
- Chunking directly affects retrieval quality.
- Batch embedding work when possible.
- Combine vector search with metadata filters when useful.
- RAG is not limited to vector databases.
- Evaluate retrieval separately from generation.

## Daily Engineering Principle

> A RAG system is only as good as the context it retrieves.
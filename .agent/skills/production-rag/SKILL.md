---
name: production-rag
description: Enterprise RAG architecture covering semantic/hierarchical chunking, hybrid search (dense + sparse BM25), Cross-Encoder reranking, vector databases, and Vectorless RAG (PageIndex).
---

# Production RAG: Vector & Vectorless (PageIndex) Architectures

This skill guides the design of enterprise retrieval-augmented generation pipelines tailored to document morphology and retrieval precision.

## Strategic Retrieval Selection

| Retrieval Paradigm | Best Suited For | Architecture Components | Limitations |
| :--- | :--- | :--- | :--- |
| **Dense Vector RAG** | Unstructured text, fuzzy semantic search, multilingual matching | Embeddings (text-embedding-3, BGE), Vector DB (Qdrant, pgvector, Pinecone) | Struggles with exact keywords, dense tables, and complex long-form documents |
| **Hybrid RAG** | Enterprise knowledge bases, legal, technical docs | Dense vectors + Sparse BM25 + Reciprocal Rank Fusion (RRF) | Requires dual indexing and weight tuning |
| **Vectorless RAG (PageIndex)** | Structured reports, financial filings (10-K), codebases, books | Hierarchical Table of Contents (TOC) tree + LLM reasoning traversal | Higher token inference latency during tree descent |

## Detailed Pipeline Stages

### 1. Ingestion & Chunking
- **Semantic Chunking:** Break text based on sentence embedding distance drops rather than fixed character counts.
- **Hierarchical (Parent-Document) Chunking:** Index small chunks (128-256 tokens) for precise vector matching, but return the larger parent chunk (1024 tokens) to the LLM for rich context.
- **Vectorless PageIndex Indexing:** Parse documents into a hierarchical section tree (H1 -> H2 -> H3 -> Page/Paragraph) with generated summaries per node.

### 2. Hybrid Retrieval & Fusion
- Compute dense similarity: $s_{dense} = \cos(v_q, v_d)$
- Compute sparse keyword score: $s_{sparse} = \text{BM25}(q, d)$
- Merge ranks via Reciprocal Rank Fusion:
  $$RRF(d) = \sum_{m \in M} \frac{1}{k + r_m(d)}$$

### 3. Post-Retrieval Reranking
- Pass top-20 retrieved candidates through a Cross-Encoder reranker (Cohere Rerank, BGE-Reranker-Large).
- Filter out candidates scoring below relevance threshold (e.g., score < 0.65).
- Return top-5 ground truth passages with exact chunk source citations.

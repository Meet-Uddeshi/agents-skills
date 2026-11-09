---
name: production-rag
description: Enterprise RAG architectures covering semantic/hierarchical chunking, hybrid search (dense + BM25), Cross-Encoder reranking, vector databases, and Vectorless RAG (PageIndex).
---

# Production RAG: Vector & Vectorless (PageIndex) Architectures

Production Retrieval-Augmented Generation (RAG) moves beyond simplistic "embed everything and cosine-similarity top-5" to resilient, document-aware architectures tailored to data morphology and precision requirements.

---

## 1. Strategic Paradigm Selection

```text
                     +-------------------------------+
                     | Incoming Enterprise Document  |
                     +-------------------------------+
                                     |
                    Is document highly structured,   
                    hierarchical (10-K, legal, code) 
                    or requiring exact table data?   
                                     |
                     +---------------+---------------+
                     |                               |
                   YES                               NO
                     |                               |
                     v                               v
    +---------------------------------+  +---------------------------------+
    | Vectorless RAG (PageIndex)      |  | Hybrid Vector RAG               |
    | - Hierarchical TOC tree index   |  | - Dense embeddings (text-emb-3)|
    | - Reasoning-based tree descent  |  | - Sparse BM25 keyword search    |
    | - Zero chunk boundary distortion|  | - Reciprocal Rank Fusion (RRF)  |
    +---------------------------------+  +---------------------------------+
```

### 1.1 Comparative Trade-off Matrix

| Feature | Dense Vector RAG | Hybrid RAG (Dense + BM25) | Vectorless RAG (PageIndex) |
| :--- | :--- | :--- | :--- |
| **Primary Index** | Vector Database (Qdrant, pgvector) | Vector DB + Inverted Index (BM25) | Hierarchical Table of Contents (TOC) Tree |
| **Best For** | Fuzzy semantic queries, chat search | Enterprise knowledge bases, tech docs | Financial filings (10-K), legal contracts, API specs |
| **Chunking Risk** | High (sentences severed across chunks) | Moderate | Zero (structural node boundaries preserved) |
| **Keyword Recall** | Poor (struggles with part #s, UUIDs) | High | High (navigates explicit section headers) |
| **Inference Cost** | Low | Low to Moderate | Moderate (requires 2-3 reasoning hops) |

---

## 2. Vectorless RAG: PageIndex Architecture

PageIndex eliminates vector databases and arbitrary token chunking for long-form, structured documents. It constructs a **Hierarchical Tree of Contents (TOC)** where an LLM navigates the document like a human analyst.

### 2.1 PageIndex Tree Construction & Traversal Algorithm
```python
from typing import Dict, List, Optional
import json

class PageIndexNode:
    def __init__(self, node_id: str, title: str, summary: str, level: int, content: str = "", children: Optional[List['PageIndexNode']] = None):
        self.node_id = node_id
        self.title = title
        self.summary = summary
        self.level = level
        self.content = content
        self.children = children or []

    def to_toc_entry(self) -> Dict:
        return {
            "node_id": self.node_id,
            "title": self.title,
            "summary": self.summary,
            "subsections": [c.to_toc_entry() for c in self.children]
        }

class PageIndexRetriever:
    def __init__(self, root: PageIndexNode):
        self.root = root

    def get_top_level_toc(self) -> List[Dict]:
        """Returns top-level table of contents for initial LLM routing."""
        return [c.to_toc_entry() for c in self.root.children]

    def select_target_nodes(self, llm_decision: List[str]) -> List[str]:
        """
        Takes LLM-selected node IDs from TOC, retrieves content, and unpacks
        exact target pages without vector distortion.
        """
        results = []
        node_map = {}

        def index_nodes(node):
            node_map[node.node_id] = node
            for child in node.children:
                index_nodes(child)

        index_nodes(self.root)

        for nid in llm_decision:
            if nid in node_map:
                target = node_map[nid]
                results.append(f"### {target.title} (Node: {target.node_id})\n{target.content}")
        return results
```

---

## 3. Hybrid RAG Architecture & Reciprocal Rank Fusion (RRF)

When dealing with unstructured knowledge bases, combining dense semantic search with sparse BM25 keyword matching prevents the "semantic drift" failure where vector cosine similarity retrieves conceptually similar but factually irrelevant documents.

### 3.1 Reciprocal Rank Fusion (RRF) Implementation
```python
from typing import Dict, List, Tuple
from collections import defaultdict

def reciprocal_rank_fusion(
    dense_results: List[Tuple[str, float]],  # (doc_id, score)
    sparse_results: List[Tuple[str, float]], # (doc_id, score)
    k: int = 60
) -> List[Tuple[str, float]]:
    """
    Fuses dense and sparse rankings using Reciprocal Rank Fusion (RRF).
    Formula: RRF_score(d) = sum(1.0 / (k + rank(d)))
    """
    rrf_scores = defaultdict(float)

    # Rank dense results
    for rank, (doc_id, _) in enumerate(dense_results):
        rrf_scores[doc_id] += 1.0 / (k + rank + 1)

    # Rank sparse results
    for rank, (doc_id, _) in enumerate(sparse_results):
        rrf_scores[doc_id] += 1.0 / (k + rank + 1)

    # Sort documents by fused RRF score
    sorted_docs = sorted(rrf_scores.items(), key=lambda item: item[1], reverse=True)
    return sorted_docs
```

---

## 4. Cross-Encoder Reranking & Quality Filters

Bi-encoders (embeddings) encode query and document independently, missing cross-attention term interactions. A **Cross-Encoder reranker** passes query and document through full self-attention layers simultaneously, producing an accurate relevance score.

```python
def apply_reranking(query: str, retrieved_docs: List[Dict], reranker_model, top_n: int = 5, score_threshold: float = 0.65) -> List[Dict]:
    """
    Applies Cross-Encoder reranking on retrieved candidates.
    Filters out passages scoring below the strict confidence threshold.
    """
    pairs = [[query, doc["content"]] for doc in retrieved_docs]
    scores = reranker_model.predict(pairs)

    reranked = []
    for doc, score in zip(retrieved_docs, scores):
        if score >= score_threshold:
            doc["rerank_score"] = float(score)
            reranked.append(doc)

    reranked.sort(key=lambda d: d["rerank_score"], reverse=True)
    return reranked[:top_n]
```

---

## 5. Grounded Citation Extraction

Every factual statement generated by the synthesis model must be attributed to an exact retrieved passage ID.

```markdown
<!-- Grounded Output Contract -->
Based on the audited financial statement, the total operating expenses for FY2025 were $412.3M [Doc-14, Section 4.2], representing an 8.4% increase over FY2024 ($380.2M) [Doc-18, Table 2.1].
```

---

## 6. Mandatory Quality Gates & Anti-Patterns

### Anti-Patterns to Avoid
- **Raw Top-k Dump:** Never feed top-5 raw vector results directly to the LLM without deduplication and reranking.
- **Fixed-Character Chunking:** Never slice documents at arbitrary 500-character boundaries without sentence or semantic boundary awareness.
- **Unverified Generation:** Never accept an answer if zero retrieved passages meet the reranker score threshold ($\ge 0.65$). In that event, trigger a "Insufficient Context" fallback.

### Verification Checklist
1. Did you evaluate document structure before choosing between Vector RAG and PageIndex?
2. Is BM25 keyword matching combined with dense vector embeddings via RRF ($k=60$)?
3. Are all candidate chunks reranked using a Cross-Encoder?
4. Are all final factual assertions grounded with verified chunk citations?

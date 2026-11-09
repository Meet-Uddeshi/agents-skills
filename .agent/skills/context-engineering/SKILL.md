---
name: context-engineering
description: Production LLM context window architecture, attention budgeting, prompt assembly, dynamic tool registries, trajectory compaction, and evaluation harnesses.
---

# Context & Harness Engineering

Context engineering governs what enters the LLM context window, when it enters, and how it is structured across multi-turn trajectories to prevent context rot, token waste, and attention degradation.

---

## 1. Attention Curve & Token Budgeting

LLMs exhibit non-uniform attention across their context window due to positional encoding decays and attention entropy. Attention is highest at the **Head** (Primacy effect) and the **Tail** (Recency effect), while information in the middle suffers from the "Lost in the Middle" phenomenon.

```text
Attention
Weight
  ^
1.0|   \                                                  /
   |    \                                                /
0.5|     \                                              /
   |      \____________________________________________/
0.0+---------------------------------------------------------> Context Position
      HEAD (System Invariants)   MIDDLE (Evidence)   TAIL (Task & Schema)
```

### 1.1 Structural Assembly Pattern
```python
def assemble_context(system_invariants: str, compressed_history: str, current_evidence: str, user_task: str, output_schema: str) -> str:
    """
    Assembles prompt strictly adhering to the Head-Middle-Tail attention curve.
    """
    prompt_parts = [
        # HEAD: Immutable constraints, zero-assumption policy, safety boundaries
        "=== SYSTEM INVARIANTS & CONSTRAINTS (HEAD) ===",
        system_invariants.strip(),
        "",
        # MIDDLE: Compressed execution history and background reference facts
        "=== CONTEXTUAL EVIDENCE & HISTORY (MIDDLE) ===",
        compressed_history.strip(),
        "",
        current_evidence.strip(),
        "",
        # TAIL: Current micro-task, immediate tool observations, exact output schema
        "=== CURRENT TASK EXECUTION & DELIVERABLES (TAIL) ===",
        user_task.strip(),
        "",
        "=== REQUIRED OUTPUT SCHEMA ===",
        output_schema.strip()
    ]
    return "\n".join(prompt_parts)
```

---

## 2. Trajectory Compaction & Truncation Policies

When long-horizon agent execution spans dozens of turns, raw tool outputs and verbose conversation logs cause context pollution and exponential cost increase.

### 2.1 Sliding Window with Semantic Rollup
```python
from typing import List, Dict

class ContextCompactor:
    def __init__(self, token_limit: int = 8000, compression_threshold: float = 0.7):
        self.token_limit = token_limit
        self.threshold = int(token_limit * compression_threshold)

    def estimate_tokens(self, text: str) -> int:
        # Fast heuristic: ~4 characters per token
        return len(text) // 4

    def compact_trajectory(self, turns: List[Dict[str, str]]) -> List[Dict[str, str]]:
        total_tokens = sum(self.estimate_tokens(t["content"]) for t in turns)
        if total_tokens <= self.threshold:
            return turns

        # Keep initial prompt (Turn 0) and latest 3 turns intact
        head = turns[:1]
        tail = turns[-3:]
        middle = turns[1:-3]

        # Summarize middle turns into concise bullet points
        summary_bullets = []
        for t in middle:
            role = t["role"]
            content = t["content"]
            # Extract key findings or tool results
            first_line = content.strip().split("\n")[0][:120]
            summary_bullets.append(f"- [{role.upper()}]: {first_line}")

        compacted_middle = [{
            "role": "system",
            "content": "=== COMPACTED TRAJECTORY SUMMARY ===\n" + "\n".join(summary_bullets)
        }]

        return head + compacted_middle + tail
```

### 2.2 Tool Output Pruning
Never inject raw HTML dumps, entire 500-line stack traces, or unfiltered JSON payloads into context:
- Strip HTML tags down to semantic text.
- Truncate stack traces to the innermost 5 stack frames.
- Filter JSON down to explicitly requested fields:
  ```python
  def prune_json(raw_data: dict, allowed_keys: list) -> dict:
      return {k: raw_data[k] for k in allowed_keys if k in raw_data}
  ```

---

### 2.3 SQLite Bounded Memory & Context Storage

To prevent unbounded Markdown bloat (such as execution logs, session failures, and architecture invariants growing beyond context limits), Meet AI Agents employs a dual-mode SQLite storage engine:

- **Storage Engine:** `.agent/memory/memory.db` with WAL mode and FTS5 full-text search.
- **Bounded Query Invariant:** Always enforce `LIMIT 5` on memory lookups:
  ```sql
  SELECT m.id, m.key, m.content, f.rank 
  FROM fts_memories f 
  JOIN memories m ON f.rowid = m.id 
  WHERE fts_memories MATCH 'invariant query' 
  ORDER BY rank LIMIT 5;
  ```
- **Dual-Mode Sync:** Keeps human-readable Markdown files (`ARCHITECTURE_MEMORY.md`, `BLACKBOARD.md`) synchronized with SQLite storage via `meet memory sync`.
- **Automated Retention:** `meet memory prune --days 30` cleans historical coordination logs while preserving architectural invariants.

---

## 3. Dynamic Tool Registry RAG

Exposing 40+ tool schemas simultaneously causes tool confusion and hallucinated arguments. Instead, index tool schemas in an in-memory vector or keyword registry and dynamically inject only the top 3-5 tools matching the current task.

```python
import re
from typing import List, Dict

class DynamicToolRegistry:
    def __init__(self):
        self.tools: Dict[str, Dict] = {}

    def register_tool(self, name: str, description: str, schema: dict):
        self.tools[name] = {"description": description, "schema": schema}

    def select_tools_for_task(self, task_description: str, max_tools: int = 4) -> List[Dict]:
        query_words = set(re.findall(r"\w+", task_description.lower()))
        scored = []
        for name, t in self.tools.items():
            desc_words = set(re.findall(r"\w+", t["description"].lower()))
            overlap = len(query_words.intersection(desc_words))
            scored.append((overlap, t["schema"]))
        
        # Sort by relevance
        scored.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored[:max_tools]]
```

---

## 4. Evaluation Harnesses (Ragas, TruLens, Inspect)

Before trusting any context strategy or prompt architecture, benchmark it against an automated evaluation harness measuring 4 core metrics:

| Metric | Target Threshold | Formula / Definition | Action if Failing |
| :--- | :--- | :--- | :--- |
| **Faithfulness** | $\ge 0.90$ | Claims grounded in context / Total claims made | Add citation enforcement; prune irrelevant context |
| **Context Recall** | $\ge 0.85$ | Ground truth sentences retrieved / Total ground truth sentences | Increase chunk overlap; tune hybrid BM25 weights |
| **Context Precision** | $\ge 0.80$ | Relevant chunks ranked at top / Total retrieved chunks | Add Cross-Encoder reranker; drop low-scoring chunks |
| **Token Efficiency** | $< 4,000$ tok/turn | Average tokens consumed per successful agent milestone | Implement sliding-window semantic rollup |

---

## 5. Mandatory Rules & Anti-Patterns

### Anti-Patterns to Strictly Avoid
- **Context Flooding:** Never pipe the output of `grep -r` or `git log` directly into an agent prompt without line limits.
- **Lost-in-the-Middle Anti-Pattern:** Never place critical system rules (e.g. "Zero emojis", "Never modify schema") in the middle of long reference text.
- **Unbounded Conversation Histories:** Never allow an agent conversation loop to exceed 30 turns without compacting history.

### Mandatory Verification Checklist
1. Are immutable system constraints anchored at the prompt Head?
2. Are tool outputs filtered and stripped of extraneous metadata before appending?
3. Does the system trigger trajectory compaction before context reaches 75% capacity?
4. Are evaluation metrics measured across a versioned baseline dataset?

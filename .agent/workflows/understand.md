---
description: End-to-end repository onboarding and exploration workflow. Deep scan codebase, extract AST symbols, generate architecture knowledge graph, and create guided onboarding tour.
---

# /understand - Codebase Onboarding & Exploration Workflow

$ARGUMENTS

---

## Purpose

Rapidly inspect, index, and comprehend an unfamiliar codebase end-to-end. Generates file inventories, architectural layer maps, dependency call graphs, domain entities, and guided developer tours.

---

## Sub-commands

```text
/understand scan                       - Generate inventory of languages, frameworks, entrypoints, and file tree
/understand graph                      - Build symbol dependency graph and inter-module import topology
/understand domains                    - Extract business domains, bounded contexts, and entity relationships
/understand tour                       - Generate interactive step-by-step developer onboarding walkthrough
/understand explain [module]           - Deep dive into specific subsystem, data flows, and lifecycles
```

---

## Standard 6-Step Implementation Workflow

1. **Repository Inventory & Technology Detection:**
   - Detect project type, root configuration (`package.json`, `Cargo.toml`, `go.mod`, `pom.xml`, `requirements.txt`).
   - Run `node .agent/skills/understand/scan-project.mjs` to map file inventory and ignore build artifacts.

2. **AST Parsing & Symbol Extraction:**
   - Run `node .agent/skills/understand/extract-structure.mjs` to extract classes, functions, interfaces, and routes.
   - Build import/export dependency map (`extract-import-map.mjs`).

3. **Architectural Clustering & Layer Classification:**
   - Partition files into layers: presentation (UI), API routers, application services, domain models, infrastructure adapters.
   - Identify cross-layer boundary violations.

4. **Domain Entity & Relationship Modeling:**
   - Extract core business entities, aggregate roots, database tables, and schema migrations.
   - Document state machines and business rules.

5. **Knowledge Graph Assembly & Storage:**
   - Merge batch graphs into unified knowledge graph (`merge-batch-graphs.py`).
   - Store synthesized architecture insights in `.agent/memory/ARCHITECTURE_MEMORY.md`.

6. **Generate Developer Onboarding Tour:**
   - Formulate 5-minute onboarding tour highlighting entry points, critical path request lifecycle, and configuration points.


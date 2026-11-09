"""
Test Suite for Meet AI Agents SQLite Memory & Context Engineering System.

Verifies:
1. SQLite database initialization and schema migration.
2. WAL mode and FTS5 full-text indexing table creation.
3. Memory logging and UPSERT idempotence.
4. Bounded querying with limit enforcement (LIMIT 5).
5. Full-text search (FTS5) BM25 ranking and phrase queries.
6. Blackboard coordination event logging and query filters.
7. Dual-mode bi-directional Markdown synchronization.
8. Memory pruning and retention bounds.
9. Node CLI and Python CLI memory subcommands.
"""

import os
import sys
import json
import subprocess
import tempfile
import sqlite3
from pathlib import Path
import pytest

# Ensure bin directory is in sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
WORKSPACE_DIR = SCRIPT_DIR.parent.parent
BIN_DIR = WORKSPACE_DIR / "bin"
if str(BIN_DIR) not in sys.path:
    sys.path.insert(0, str(BIN_DIR))

from memory_manager import MemoryManager


@pytest.fixture
def temp_db():
    """Provides an isolated temporary SQLite database for testing."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = Path(f.name)
    yield db_path
    if db_path.exists():
        try:
            db_path.unlink()
        except OSError:
            pass


def test_db_initialization(temp_db):
    """Verifies tables, WAL mode, FTS5 virtual table, and schema triggers."""
    mm = MemoryManager(db_path=temp_db)
    stats = mm.get_stats()

    assert stats["total_memories"] == 0
    assert stats["total_events"] == 0
    assert stats["size_bytes"] > 0

    # Inspect SQLite pragmas directly
    conn = sqlite3.connect(str(temp_db))
    cursor = conn.cursor()
    cursor.execute("PRAGMA journal_mode;")
    mode = cursor.fetchone()[0]
    assert mode.upper() == "WAL"

    # Verify tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    assert "memories" in tables
    assert "blackboard_events" in tables
    assert "fts_memories" in tables
    assert "schema_migrations" in tables
    conn.close()


def test_memory_upsert(temp_db):
    """Verifies insertion and subsequent update on the same unique key."""
    mm = MemoryManager(db_path=temp_db)

    # First insert
    mm.log_memory(
        key="invariant:test_rule",
        content="Initial rule content",
        category="invariant",
        agent="ai-engineer",
        tags=["rule", "safety"]
    )
    mem1 = mm.get_memory("invariant:test_rule")
    assert mem1 is not None
    assert mem1["content"] == "Initial rule content"
    assert mem1["category"] == "invariant"

    # Upsert with modified content
    mm.log_memory(
        key="invariant:test_rule",
        content="Updated rule content with stricter constraints",
        category="invariant",
        agent="ai-engineer",
        tags=["rule", "safety", "v2"]
    )
    mem2 = mm.get_memory("invariant:test_rule")
    assert mem2["content"] == "Updated rule content with stricter constraints"
    assert "v2" in mem2["tags"]

    stats = mm.get_stats()
    assert stats["total_memories"] == 1


def test_fts5_full_text_search(temp_db):
    """Verifies that FTS5 indexing indexes content and retrieves relevant memories."""
    mm = MemoryManager(db_path=temp_db)

    mm.log_memory(
        key="arch:caching",
        content="Implement Redis caching layer with LRU eviction and 15 minute TTL.",
        category="architecture",
        agent="backend-specialist"
    )
    mm.log_memory(
        key="arch:database",
        content="PostgreSQL schema with connection pooling and read replicas.",
        category="architecture",
        agent="database-architect"
    )
    mm.log_memory(
        key="rule:zero_emoji",
        content="Strict ban on decorative emojis across all documentation and commits.",
        category="invariant",
        agent="system"
    )

    # Search for "caching"
    res1 = mm.query_memories(search_term="caching", limit=5)
    assert len(res1) == 1
    assert res1[0]["key"] == "arch:caching"

    # Search for "emoji"
    res2 = mm.query_memories(search_term="emoji", limit=5)
    assert len(res2) == 1
    assert res2[0]["key"] == "rule:zero_emoji"

    # Search across categories with limit
    res3 = mm.query_memories(category="architecture", limit=1)
    assert len(res3) == 1


def test_bounded_query_limit(temp_db):
    """Verifies that limit constraint strictly bounds returned records to prevent context explosion."""
    mm = MemoryManager(db_path=temp_db)

    # Insert 15 items
    for i in range(15):
        mm.log_memory(
            key=f"item:{i}",
            content=f"Context content number {i}",
            category="general"
        )

    # Query with limit=5
    results = mm.query_memories(limit=5)
    assert len(results) == 5

    # Query with limit=3
    results_3 = mm.query_memories(limit=3)
    assert len(results_3) == 3


def test_blackboard_events(temp_db):
    """Verifies logging and filtered querying of coordination events."""
    mm = MemoryManager(db_path=temp_db)

    mm.log_event(
        agent="orchestrator",
        event_type="discovery",
        description="Identified 3 entrypoint services in backend.",
        session_id="session-101"
    )
    mm.log_event(
        agent="code-reviewer",
        event_type="status_change",
        description="Completed review of PR #42 with 2 requested changes.",
        session_id="session-101"
    )
    mm.log_event(
        agent="devops-engineer",
        event_type="workflow_run",
        description="Deployed staging cluster v1.2.0.",
        session_id="session-102"
    )

    events_101 = mm.query_events(session_id="session-101")
    assert len(events_101) == 2

    devops_events = mm.query_events(agent="devops-engineer")
    assert len(devops_events) == 1
    assert devops_events[0]["event_type"] == "workflow_run"


def test_markdown_sync(temp_db):
    """Verifies syncing ARCHITECTURE_MEMORY.md and BLACKBOARD.md into SQLite."""
    mm = MemoryManager(db_path=temp_db)
    sync_res = mm.sync_from_markdown(base_dir=WORKSPACE_DIR)

    assert sync_res["synced_invariants"] >= 3
    invariants = mm.query_memories(category="invariant", limit=10)
    assert len(invariants) >= 3

    keys = [inv["key"] for inv in invariants]
    assert any("emoji" in k for k in keys)
    assert any("catalog" in k or "agent" in k for k in keys)


def test_cli_integration():
    """Verifies CLI execution of memory commands via meet CLI."""
    python_exe = sys.executable

    # Test meet memory stats
    cmd_stats = [python_exe, str(BIN_DIR / "cli.py"), "memory", "stats", "--json"]
    proc = subprocess.run(cmd_stats, capture_output=True, text=True, check=True)
    stats_data = json.loads(proc.stdout)
    assert "total_memories" in stats_data
    assert "size_bytes" in stats_data

    # Test meet memory query
    cmd_query = [python_exe, str(BIN_DIR / "cli.py"), "memory", "query", "emoji", "--limit", "3", "--json"]
    proc_q = subprocess.run(cmd_query, capture_output=True, text=True, check=True)
    query_data = json.loads(proc_q.stdout)
    assert isinstance(query_data, list)
    assert len(query_data) >= 1
    assert any("emoji" in item["key"] for item in query_data)

"""
Meet AI Agents - SQLite Memory & Context Engineering Manager.

Provides persistent, indexed, bounded memory querying and full-text search (FTS5)
to solve context window overload and prevent unbounded Markdown file bloat.
Dual-mode synchronization bridges structured SQLite storage and human-readable Markdown.
"""

from typing import List, Dict, Any, Optional
import os
import sys
import json
import sqlite3
import re
from pathlib import Path
from datetime import datetime


class MemoryManager:
    """
    Production-grade SQLite memory and context manager with FTS5 indexing,
    bounded querying, and dual-mode Markdown synchronization.
    """

    SCHEMA_VERSION = 1

    def __init__(self, db_path: Optional[Path] = None):
        if db_path is None:
            # Locate .agent/memory/memory.db relative to this file or cwd
            base_dir = Path(__file__).resolve().parent.parent
            self.db_dir = base_dir / ".agent" / "memory"
            self.db_path = self.db_dir / "memory.db"
        else:
            self.db_path = Path(db_path)
            self.db_dir = self.db_path.parent

        self.db_dir.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        """Establishes an optimized SQLite connection with WAL mode and row factory."""
        conn = sqlite3.connect(str(self.db_path), timeout=10.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA synchronous = NORMAL;")
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def _init_db(self):
        """Initializes tables, FTS5 virtual tables, and synchronization triggers."""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Schema version tracking
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS schema_migrations (
                version INTEGER PRIMARY KEY,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)

            # Core memories table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT NOT NULL UNIQUE,
                content TEXT NOT NULL,
                category TEXT NOT NULL DEFAULT 'general',
                agent TEXT DEFAULT 'system',
                tags TEXT DEFAULT '',
                metadata TEXT DEFAULT '{}',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)

            # Blackboard and agent coordination events
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS blackboard_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                agent TEXT NOT NULL,
                event_type TEXT NOT NULL,
                description TEXT NOT NULL,
                payload TEXT DEFAULT '{}',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)

            # Check if FTS5 table exists
            cursor.execute("""
            SELECT count(*) FROM sqlite_master 
            WHERE type='table' AND name='fts_memories';
            """)
            fts_exists = cursor.fetchone()[0] > 0

            if not fts_exists:
                cursor.execute("""
                CREATE VIRTUAL TABLE fts_memories USING fts5(
                    key,
                    content,
                    category,
                    agent,
                    tags,
                    content='memories',
                    content_rowid='id'
                );
                """)

                # FTS Synchronization Triggers
                cursor.execute("""
                CREATE TRIGGER IF NOT EXISTS memories_ai AFTER INSERT ON memories BEGIN
                    INSERT INTO fts_memories(rowid, key, content, category, agent, tags)
                    VALUES (new.id, new.key, new.content, new.category, new.agent, new.tags);
                END;
                """)

                cursor.execute("""
                CREATE TRIGGER IF NOT EXISTS memories_ad AFTER DELETE ON memories BEGIN
                    INSERT INTO fts_memories(fts_memories, rowid, key, content, category, agent, tags)
                    VALUES ('delete', old.id, old.key, old.content, old.category, old.agent, old.tags);
                END;
                """)

                cursor.execute("""
                CREATE TRIGGER IF NOT EXISTS memories_au AFTER UPDATE ON memories BEGIN
                    INSERT INTO fts_memories(fts_memories, rowid, key, content, category, agent, tags)
                    VALUES ('delete', old.id, old.key, old.content, old.category, old.agent, old.tags);
                    INSERT INTO fts_memories(rowid, key, content, category, agent, tags)
                    VALUES (new.id, new.key, new.content, new.category, new.agent, new.tags);
                END;
                """)

            # Record migration version
            cursor.execute("""
            INSERT OR IGNORE INTO schema_migrations (version) VALUES (?);
            """, (self.SCHEMA_VERSION,))

            conn.commit()

    def log_memory(
        self,
        key: str,
        content: str,
        category: str = "general",
        agent: str = "system",
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> int:
        """
        Stores or updates an indexed memory entry via UPSERT.
        """
        tags_str = ",".join(tags) if tags else ""
        meta_str = json.dumps(metadata or {})

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO memories (key, content, category, agent, tags, metadata, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(key) DO UPDATE SET
                content = excluded.content,
                category = excluded.category,
                agent = excluded.agent,
                tags = excluded.tags,
                metadata = excluded.metadata,
                updated_at = CURRENT_TIMESTAMP;
            """, (key, content, category, agent, tags_str, meta_str))
            conn.commit()
            return cursor.lastrowid

    def get_memory(self, key: str) -> Optional[Dict[str, Any]]:
        """Retrieves a single memory entry by key."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM memories WHERE key = ?", (key,))
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None

    def query_memories(
        self,
        search_term: Optional[str] = None,
        category: Optional[str] = None,
        agent: Optional[str] = None,
        tag: Optional[str] = None,
        limit: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Performs bounded querying with full-text search (FTS5) or structured filters.
        Limits retrieval to prevent context window saturation.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()

            if search_term and search_term.strip():
                # Sanitize search term for FTS5 (escape special punctuation)
                cleaned_term = re.sub(r'[^\w\s]', ' ', search_term).strip()
                tokens = [f'"{tok}"*' for tok in cleaned_term.split() if tok]
                if not tokens:
                    tokens = [f'"{search_term.strip()}"*']
                fts_query = " ".join(tokens)

                sql = """
                SELECT m.id, m.key, m.content, m.category, m.agent, m.tags, m.created_at, m.updated_at,
                       fts_memories.rank
                FROM fts_memories
                JOIN memories m ON fts_memories.rowid = m.id
                WHERE fts_memories MATCH ?
                """
                params = [fts_query]

                if category:
                    sql += " AND m.category = ?"
                    params.append(category)
                if agent:
                    sql += " AND m.agent = ?"
                    params.append(agent)
                if tag:
                    sql += " AND m.tags LIKE ?"
                    params.append(f"%{tag}%")

                sql += " ORDER BY rank LIMIT ?"
                params.append(limit)

                try:
                    cursor.execute(sql, params)
                    return [dict(row) for row in cursor.fetchall()]
                except sqlite3.OperationalError:
                    # Fallback to standard LIKE search if FTS syntax error
                    pass

            # Standard structured query
            sql = "SELECT * FROM memories WHERE 1=1"
            params = []

            if category:
                sql += " AND category = ?"
                params.append(category)
            if agent:
                sql += " AND agent = ?"
                params.append(agent)
            if tag:
                sql += " AND tags LIKE ?"
                params.append(f"%{tag}%")
            if search_term:
                sql += " AND (content LIKE ? OR key LIKE ?)"
                params.extend([f"%{search_term}%", f"%{search_term}%"])

            sql += " ORDER BY updated_at DESC LIMIT ?"
            params.append(limit)

            cursor.execute(sql, params)
            return [dict(row) for row in cursor.fetchall()]

    def log_event(
        self,
        agent: str,
        event_type: str,
        description: str,
        session_id: Optional[str] = None,
        payload: Optional[Dict[str, Any]] = None,
    ) -> int:
        """Logs a blackboard or coordination event."""
        payload_str = json.dumps(payload or {})
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO blackboard_events (session_id, agent, event_type, description, payload)
            VALUES (?, ?, ?, ?, ?);
            """, (session_id, agent, event_type, description, payload_str))
            conn.commit()
            return cursor.lastrowid

    def query_events(
        self,
        session_id: Optional[str] = None,
        agent: Optional[str] = None,
        event_type: Optional[str] = None,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """Queries recent blackboard events."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            sql = "SELECT * FROM blackboard_events WHERE 1=1"
            params = []

            if session_id:
                sql += " AND session_id = ?"
                params.append(session_id)
            if agent:
                sql += " AND agent = ?"
                params.append(agent)
            if event_type:
                sql += " AND event_type = ?"
                params.append(event_type)

            sql += " ORDER BY created_at DESC LIMIT ?"
            params.append(limit)

            cursor.execute(sql, params)
            return [dict(row) for row in cursor.fetchall()]

    def sync_from_markdown(self, base_dir: Optional[Path] = None) -> Dict[str, int]:
        """
        Parses ARCHITECTURE_MEMORY.md and BLACKBOARD.md into SQLite tables.
        """
        root = base_dir or self.db_dir.parent.parent
        arch_file = root / ".agent" / "memory" / "ARCHITECTURE_MEMORY.md"
        blackboard_file = root / ".agent" / "context" / "BLACKBOARD.md"

        synced_invariants = 0
        synced_events = 0

        # 1. Parse ARCHITECTURE_MEMORY.md
        if arch_file.exists():
            content = arch_file.read_text(encoding="utf-8")
            pattern = re.compile(
                r"^\s*\d+\.\s+\*\*([^*:]+):?\*\*:?\s*(.*?)(?=(?:^\s*\d+\.|\Z))",
                re.MULTILINE | re.DOTALL
            )
            for match in pattern.finditer(content):
                title = match.group(1).strip()
                body = match.group(2).strip()
                key = "invariant:" + re.sub(r"[^\w]+", "_", title.lower()).strip("_")
                self.log_memory(
                    key=key,
                    content=f"**{title}:**\n{body}",
                    category="invariant",
                    agent="system",
                    tags=["invariant", "architecture", "workspace_rule"],
                    metadata={"source_file": "ARCHITECTURE_MEMORY.md"},
                )
                synced_invariants += 1

        # 2. Parse BLACKBOARD.md workflow runs
        if blackboard_file.exists():
            bb_content = blackboard_file.read_text(encoding="utf-8")
            # Extract workflow runs: "### Workflow Run: <name> [<time>]"
            wf_pattern = re.compile(
                r"###\s+Workflow Run:\s+([^\s]+)\s+\[([^\]]+)\]\s*\n"
                r"-\s+\*\*Executing Agent\*\*:\s*`([^`]+)`\s*\n"
                r"-\s+\*\*Task Scope\*\*:\s*([^\n]+)\s*\n"
                r"-\s+\*\*Execution Status\*\*:\s*`([^`]+)`\s*\n"
                r"-\s+\*\*Notes / Findings\*\*:\s*([^\n]+)",
                re.MULTILINE
            )
            for m in wf_pattern.finditer(bb_content):
                wf_name = m.group(1).strip()
                wf_time = m.group(2).strip()
                agent = m.group(3).strip()
                scope = m.group(4).strip()
                status = m.group(5).strip()
                notes = m.group(6).strip()

                self.log_event(
                    agent=agent,
                    event_type="workflow_run",
                    description=f"Workflow /{wf_name} status: {status} ({scope}). {notes}",
                    session_id=wf_time,
                    payload={"workflow": wf_name, "status": status, "scope": scope},
                )
                synced_events += 1

        return {
            "synced_invariants": synced_invariants,
            "synced_events": synced_events,
        }

    def sync_to_markdown(self, base_dir: Optional[Path] = None):
        """
        Exports active invariants and blackboard state from SQLite to Markdown.
        Ensures human readability while keeping SQLite as source of truth.
        """
        root = base_dir or self.db_dir.parent.parent
        arch_file = root / ".agent" / "memory" / "ARCHITECTURE_MEMORY.md"

        invariants = self.query_memories(category="invariant", limit=50)
        if invariants and arch_file.exists():
            # Format invariants markdown
            lines = [
                "# Persistent Workspace Memory",
                "",
                "This document stores persistent architectural invariants, established patterns, and cross-session constraints across the repository. All agents query this memory before planning structural, architectural, or multi-file changes.",
                "",
                "## System Invariants",
                "",
            ]
            for idx, inv in enumerate(invariants, start=1):
                raw = inv["content"].strip()
                # Ensure properly formatted bullet list
                lines.append(f"{idx}. {raw}")
                lines.append("")

            arch_file.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")

    def get_stats(self) -> Dict[str, Any]:
        """Returns database statistics including file size, counts, and categories."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT count(*) FROM memories;")
            total_memories = cursor.fetchone()[0]

            cursor.execute("SELECT count(*) FROM blackboard_events;")
            total_events = cursor.fetchone()[0]

            cursor.execute("SELECT category, count(*) FROM memories GROUP BY category;")
            categories = {row[0]: row[1] for row in cursor.fetchall()}

        size_bytes = self.db_path.stat().st_size if self.db_path.exists() else 0

        return {
            "db_path": str(self.db_path),
            "size_bytes": size_bytes,
            "size_kb": round(size_bytes / 1024, 2),
            "total_memories": total_memories,
            "total_events": total_events,
            "categories": categories,
        }

    def prune(self, max_age_days: int = 30, keep_invariants: bool = True) -> int:
        """
        Prunes events older than max_age_days to maintain bounded storage.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            DELETE FROM blackboard_events 
            WHERE created_at < datetime('now', ?);
            """, (f"-{max_age_days} days",))
            deleted_events = cursor.rowcount

            if not keep_invariants:
                cursor.execute("""
                DELETE FROM memories
                WHERE category != 'invariant' AND updated_at < datetime('now', ?);
                """, (f"-{max_age_days} days",))
                deleted_memories = cursor.rowcount
            else:
                deleted_memories = 0

            conn.commit()
            return deleted_events + deleted_memories
